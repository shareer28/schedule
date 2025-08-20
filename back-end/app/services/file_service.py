import duckdb
from duckdb.typing import VARCHAR, TIMESTAMP, DATE
from fastapi import UploadFile, BackgroundTasks

from app.duckdb import read_file
from app.utils import get_mappings, get_examples, run_retry, get_csv
from app.agents import get_column_mapping_agent, get_transformation_agent, get_translation_agent
from app.google.sheets.service import get_organizations, get_specialisms, append_values, remove_rows_by_org_and_filename
from logging import getLogger, ERROR

logger = getLogger(__name__)

def transform_file(
    file : UploadFile, 
    organisation_id: str,
    background_tasks: BackgroundTasks
):
    organizations = get_organizations().organizations
    organization = None
    for o in organizations :
        if o.id == organisation_id:
            organization = o
            break
    specialisms = get_specialisms().specialisms

    if not organization:
        logger.log(ERROR, "Organisation does not exist")
        return 

    conn = duckdb.connect(database=":memory:"); 
    table_name = read_file(file, conn)
    
    mappings = get_mappings(conn)
    examples = get_examples(conn)
    mappings = {
        "theatre":  VARCHAR,
        "actual_start_case_datetime": TIMESTAMP,
        "actual_end_case_datetime": TIMESTAMP,
        "date": DATE,
        "specialism_name": VARCHAR,
        "procedure_name": VARCHAR
    }

    column_renaming_agent = get_column_mapping_agent(table_name, list(mappings.keys()), mappings, examples)
    result = run_retry(
        column_renaming_agent,
        get_csv(conn, f"SELECT * FROM '{table_name}' USING SAMPLE 50"), 
        conn
    )

    result_table = "MappingResult"
    conn.sql(f"CREATE TABLE {result_table} AS {result}")

    rules = [
        "Use TIMESTAMP and DATE format fuctions when from NVARCHAR to TIMESTAMP or DATE.",
        "For TIMESTAMP types, check if you can parse the timestamp with a basic pattern such as '%d-%m-%Y %H:%M:%S', '%d/%m/%Y %H:%M' and adapt from there.",
        "For the theatre, try to remove trailing zero's after the last . and the . itself",
        "For actual_case_datetimes, filter null values"
        "Reduce the duplicate rows to a single row",
    ]
    transforming_agent = get_transformation_agent(result_table, rules, mappings, conn)
    result = run_retry(
        transforming_agent, 
        get_csv(conn, f"SELECT * FROM '{result_table}' USING SAMPLE 100"), 
        conn
    )

    result_table = "MappingResultTranslations"
    conn.sql(f"CREATE TABLE {result_table} AS { result.replace(";", "") } ")

    translating_agent = get_translation_agent(result_table, conn, specialisms)
    result = run_retry(
        translating_agent,
        get_csv(conn, f"SELECT * FROM '{result_table}' USING SAMPLE 100"), 
        conn
    )   

    # Now processing the items
    turnover_data = conn.sql(
        f"""
        WITH transformed_dataset AS (
        { result.replace(";", "") }        
        ),
        turnover_dataset AS (
            SELECT *
                , row_number() OVER (PARTITION BY theatre, date ORDER BY actual_end_case_datetime) AS actual_day_sequence_number
                , lag(actual_end_case_datetime) OVER (PARTITION BY theatre, date ORDER BY actual_end_case_datetime) AS actual_previous_end_case_datetime
                , actual_start_case_datetime - actual_previous_end_case_datetime AS actual_turnovertime 
                , minute(actual_turnovertime) + 60 * hour(actual_turnovertime) AS actual_turnovertime_minutes
            FROM transformed_dataset
        )
        SELECT 
            '{organization.name}' AS organisation_name,
            '{organization.id}' AS organisation_id, 
            '{file.filename}' AS filename, 
            *
        FROM turnover_dataset
        ORDER BY theatre, actual_start_case_datetime
        """    
    )

    # Here the google call
    turnover_data_df = turnover_data.df()
    turnover_data_nl_df = turnover_data_df.copy().drop(columns=["specialism_name"]).rename(columns={ "specialism_name_nl" : "specialism_name"})
    turnover_data_en_df = turnover_data_df.copy().drop(columns=["specialism_name_nl"])
    background_tasks.add_task(append_values, "Turnovertime_NL", turnover_data_nl_df)
    background_tasks.add_task(append_values, 'Turnovertime_EN', turnover_data_en_df)

    delay_df = conn.sql(f"""
        WITH add_expected_day_start AS (
            SELECT 
                *, 
                CAST(date AS TIMESTAMP) + INTERVAL 8 HOUR AS expected_day_start,
                CAST(date AS TIMESTAMP) + INTERVAL 16 HOUR AS expected_day_end 
            FROM turnover_data_df
            WHERE actual_start_case_datetime IS NOT NULL
        ),
        difference_day AS (
            SELECT 
                *,
                IF(
                    actual_start_case_datetime < expected_day_start, 
                    expected_day_start - actual_start_case_datetime, 
                    actual_start_case_datetime - expected_day_start
                ) AS difference_day_start,
                IF(
                    actual_end_case_datetime < expected_day_end, 
                    expected_day_end - actual_end_case_datetime, 
                    actual_end_case_datetime - expected_day_end
                ) AS difference_day_end,
                IF(
                    actual_start_case_datetime < expected_day_start, 
                    'Before', 
                    'After'
                ) AS day_start_difference_type,
                IF(
                    actual_end_case_datetime < expected_day_end, 
                    'Before',
                    'After'
                ) AS day_end_difference_type,
                (expected_day_start < actual_start_case_datetime)::INT AS day_start_overtime_indicator,
                (actual_start_case_datetime < expected_day_end AND expected_day_end < actual_end_case_datetime)::INT AS day_end_overtime_indicator
            FROM add_expected_day_start
        ),
        case_duration AS (
            SELECT *
            , actual_end_case_datetime - actual_start_case_datetime AS case_duration
            , hour(case_duration) * 60 + minute(case_duration) AS case_duration_minutes
            FROM difference_day
        ),
        start_delay_start_end AS (
            SELECT 
                '{organization.name}' AS organisation_name,
                '{organization.id}' AS organisation_id, 
                '{file.filename.strip()}' AS filename, 
                theatre,
                date,
                first(day_start_difference_type ORDER BY actual_day_sequence_number ASC) AS day_start_timeline_type,
                first(day_end_difference_type ORDER BY day_end_overtime_indicator DESC, difference_day_end ASC) AS day_end_timeline_type,
                first(procedure_name ORDER BY actual_day_sequence_number ASC) AS day_start_procedure_name,
                first(procedure_name ORDER BY day_end_overtime_indicator DESC, difference_day_end ASC) AS day_end_procedure_name,
                first(actual_start_case_datetime ORDER BY actual_day_sequence_number ASC) AS actual_day_start,
                first(actual_end_case_datetime ORDER BY day_end_overtime_indicator DESC, difference_day_end ASC) AS actual_day_end,
                first(expected_day_start) AS expected_day_start,
                first(expected_day_end) AS expected_day_end,
                first(specialism_name_nl ORDER BY actual_day_sequence_number ASC) AS day_start_specialism_nl,
                first(specialism_name ORDER BY actual_day_sequence_number ASC) AS day_start_specialism,
                first(specialism_name_nl ORDER BY day_end_overtime_indicator DESC, difference_day_end ASC) AS day_end_specialism_nl,
                first(specialism_name ORDER BY day_end_overtime_indicator DESC, difference_day_end ASC) AS day_end_specialism,
                max(day_start_overtime_indicator) AS day_start_overtime_indicator,
                max(day_end_overtime_indicator) AS day_end_overtime_indicator,
                first(difference_day_start ORDER BY actual_day_sequence_number ASC) AS difference_day_start, 
                min(difference_day_end) AS difference_day_end,
                sum(case_duration_minutes) AS total_case_duration_minutes,
                ifnull(
                    sum(
                        if(
                            actual_turnovertime_minutes <= 90 AND actual_turnovertime_minutes >= -90, 
                            actual_turnovertime_minutes, 
                            0
                        )
                    ),
                    0
                ) AS total_turnovertime_minutes,
                count(*) AS number_of_cases
            FROM case_duration
            GROUP BY theatre, date
        ),
        difference_day_start_day_end AS (
            SELECT 
                *,
                minute(difference_day_start) + hour(difference_day_start) * 60 AS difference_minutes_day_start,
                minute(difference_day_end) + hour(difference_day_end) * 60 AS difference_minutes_day_end
            FROM start_delay_start_end
        ),
        formatted_data AS (
            SELECT 
                organisation_name,
                organisation_id,
                filename,
                theatre,
                date,
                total_case_duration_minutes,
                total_turnovertime_minutes,
                number_of_cases,
                actual_day_start,
                expected_day_start,
                actual_day_end,
                expected_day_end,
                day_start_timeline_type,
                day_end_timeline_type,
                day_start_procedure_name,
                day_end_procedure_name,
                day_start_specialism,
                day_start_specialism_nl,
                day_end_specialism,
                day_end_specialism_nl,
                day_start_overtime_indicator,
                day_end_overtime_indicator,
                difference_day_start,
                difference_day_end,
                difference_minutes_day_start,
                difference_minutes_day_end
            FROM
                difference_day_start_day_end
        )
        SELECT *
        FROM formatted_data
        ORDER BY actual_day_start, theatre DESC
""").df()
    
    delay_nl_df = (
        delay_df
        .copy()
        .drop(columns=["day_start_specialism", "day_end_specialism"])
        .rename(columns=
            { 
            "day_start_specialism_nl" : "day_start_specialism",
            "day_end_specialism_nl" : "day_end_specialism"
            }
        )
    )
    delay_df = delay_df.drop(columns=["day_start_specialism_nl", "day_end_specialism_nl"])
    background_tasks.add_task(append_values, "Delays_NL", delay_nl_df)
    background_tasks.add_task(append_values, 'Delays_EN', delay_df)

    conn.close()
    return