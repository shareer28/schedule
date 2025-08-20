from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env'),
        env_ignore_empty=True,
        env_file_encoding='utf-8',
        env_override=True
    )
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str
    GOOGLE_SHEET: str

settings = Settings() # type: ignore
