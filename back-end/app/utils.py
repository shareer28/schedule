import io

from pydantic_ai.models import Model 
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai import Agent

from duckdb import DuckDBPyConnection, Error

from app.core.config import settings
from logging import getLogger, ERROR
logger = getLogger(__name__)

def get_model() -> Model:
    return OpenAIModel("gpt-4.1", provider=OpenAIProvider(api_key=settings.OPENAI_API_KEY))

# def get_schema(conn : DuckDBPyConnection, query: str) -> str: 

def get_mappings(conn : DuckDBPyConnection) -> str:
    return get_csv(conn, "SELECT * FROM read_csv('./data/mapping.csv')")

def get_examples(conn : DuckDBPyConnection) -> str:
    return get_csv(conn, "SELECT * FROM read_csv('./data/examples.csv') USING SAMPLE 20")

def get_schema(conn : DuckDBPyConnection, query) -> str:
    return get_csv(conn, f"DESCRIBE {f"({query})" if "SELECT" in query else query}")

def get_csv(conn : DuckDBPyConnection, query : str) -> str:
    output = io.StringIO()
    conn.sql(f"SELECT * FROM ({query})").to_df().drop_duplicates().to_csv(output, index=False)
    result = output.getvalue()
    output.close()
    return result

def run_retry(agent : Agent, prompt: str, conn: DuckDBPyConnection) -> str:
    messages = []
    current_prompt = prompt
    for _ in range(0, 10):
        result = agent.run_sync(current_prompt, message_history=messages)
        exception = ""
        try:
             conn.sql(result.output).df()
        except Error as e:
            exception = str(e)
            logger.log(ERROR, f"Error: {exception}")
            current_prompt = exception
            messages = result.all_messages()
        if not (exception):
            break

    return result.output