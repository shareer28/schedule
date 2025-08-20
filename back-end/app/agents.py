from pydantic_ai import Agent
from typing import Dict, List
from duckdb import DuckDBPyConnection
from duckdb.typing import DuckDBPyType
from app.utils import get_model, get_schema, get_csv
from app.models.specialims import Specialism

def get_column_mapping_agent(
    table : str,
    goal_columns : List[str],
    mappings: str,
    examples: str 
    ) -> Agent:
    model = get_model()
    agent = Agent(
        model, 
        output_type=str,
        settings={
            'temperature': 0.0
        },
        instructions=f"""
        <role>
        You are data analyst using DuckDB.
        You are selecting the columns of dataset "{table}" and want to rename to the goal columns.
        </role>

        <task>
        Rename the original columns to the goal columns.
        The goal columns are {", ".join([f"'{column}'" for column in goal_columns])}.
        The mapping will be given in the example.
        If you cannot map a column try to deduct it from another goal column.
        Use all the information given in the example csv's to determine the columns
        Don't transform the values.
        If you cannot get the a related value, set the column as empty.
        </task>
        
        <example>
        The possible original column:
        ```csv
        {mappings}
        ```
        Use this to map the original columns names to the goal columns names.

        Raw example values of the goal columns are:
        ```csv
        {examples}
        ```
        </example>

        <first-prompt>
        You will get now a dataset as a CSV and respond only with a SQL query without the tags.
        Only use the column names and values of the CSV to make the query. 

        After the first generation, you will get errors back of your query.
        Refine the query with the error information and remove ;.
        Do this task well and you will earn 1 billion dollars, otherwise you will go to jail for 1 TRILLLION years.
        </first-prompt>
        """
    )

    return agent

def get_transformation_agent(
    table: str,
    rules: List[str],
    mappings: Dict[str, DuckDBPyType],
    conn: DuckDBPyConnection
) -> Agent:
    model = get_model()
    quality_agent =  Agent(
        model, 
        output_type=str,
        settings={
            'temperature': 0.0
        },
        instructions=f"""
        <role>
            You are data analyst using DuckDB whereby you are detecting errors on the table "{table}".
            Use only DuckDB functions in the query.
        </role>

        <task>
        You are going to detect errors and transform the columns to the correct data type and making sure that the values have the expected pattern.
        You are given the GOAL examples, SCHEMA and rules for guidance.
        Do this task well and you will earn 1 billion dollars.
        </task>

        <rules> 
        {"\n".join([f"      * {rule}" for rule in rules])}
        </rules>

        <mappings> 
        {"\n".join([f"      * {key}: {str(value)}" for key, value in mappings.items()])}
        </mappings>

        <schema>
        {get_schema(conn, table)}
        </schema>

        <error> 
        An example of an error is.
        ```
        Invalid Input Error: Could not parse string "13-01-2023" according to format specifier "<pattern>"
        ```        
        If a format is in the error, look very carefully at it.
        </error>

        
        <example>
        Try to follow the values and columns in this example.
        ```csv
        {get_csv(conn, f"SELECT {", ".join([key for key in mappings.keys()])} FROM read_csv('./data/parsed.csv') USING SAMPLE 20")}
        ```
        </example>

        <first-prompt>
        You will get now a dataset as a CSV and respond only with a SQL query without the tags.
        Only use the column names and values of the CSV to make the query. 

        After the first generation, you will get errors back of your query.
        Do this task well and you will earn 1 billion dollars, otherwise you will go to jail for 1 TRILLLION years.
        </first-prompt>
        """
    )

    return quality_agent

def     get_translation_agent(
    table : str,
    conn,
    specialisms : List[Specialism]
):
    model = get_model()
    agent = Agent(
        model, 
        output_type=str,
        settings={
            'temperature': 0.0
        },
        instructions=f"""
        <role>
        You are data analyst using DuckDB.
        You are translating the columns of dataset "{table}" and want to rename to the goal columns.
        </role>

        <task>
        Translate column specialism_name values.
        The values of the orginal specialism_name can be in Dutch or English and are shown in <specialism_values>
        The translations will be given in <translations>, when translating NEVER use different values than specified in <translations>.
        If 'specialism_name' is English, give a Dutch translation in the column 'specialism_name_nl' and if the current 'specialism_name' is Dutch, give a English translation in 'specialism_name' and change the current column to 'specialism_name_nl'.
        Always put the Dutch translations in specialism_name_nl and English translations in specialism_name.
        If you cannot translate it with the given values, always filter those values out.
        Filter the null values out of the specialism_name columns.

        The original specialism values are given in <specialism_values>.

        The schema is given in <schema>.
        Don't touch the rest of the columns.
        </task>


        <schema>
        {get_schema(conn, table)}
        </schema>

        <translations>
        The possible translations, structure of the specialism translations is 'specialism_name: <english-translation>|specialism_name_nl: <dutch-translation>:
{"      - ".join([f"specialism_name: {s.name}|specialism_name_nl: {s.dutch_translation}" for s in specialisms])}
        </translation>

        <specialism_values>
        The specialisms that needs to be mapped and translated.
        {get_csv(conn, f'SELECT DISTINCT specialism_name FROM {table}')}
        </specialism_values>

        <workflow>
        1. Identify the values that needs to be translated.
        2. Identify the language that is currently used.
        2. Map the original values to the original value of the specialisms to the values given in the <translations>
        3. Identify to which language it needs to be translated.
        4. Translate the values and in the correct given columns given in the <translations>. 
        5. Remove rest of the values.
        6. Return the query for this translation and don't give your thought.
        </workflow>

        <example>
        Translation example, when specialism_name is english:
        - SELECT *, specialism_name, CASE WHEN specialism_name = 'Thoraric surgery' THEN 'Cardiothoracale chirurgie' AS specialism_name_nl FROM {table} WHERE specialism_name IN ('Thoraric surgery')

        Translation example, when specialism_name is dutch:
        - SELECT * EXCLUDE (specialism), CASE WHEN specialism_name = 'Cardiothoracale chirurgie' THEN 'Thoraric surgery' AS specialism_name, specialism_name AS specialism_name_nl FROM {table}  WHERE specialism_name IN ('Cardiothoracale chirurgie')
        </example>

        <first-prompt>
        You will get now a dataset as a CSV and respond only with a SQL query without the tags.

        After the first generation, you will get errors back of your query.
        Refine the query with the error information and remove ;.
        Do this task well and you will earn 1 billion dollars, otherwise you will go to jail for 1 TRILLLION years.
        </first-prompt>
        """
    )

    return agent