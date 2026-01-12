import os
from loguru import logger
from pydantic import  Field,field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",env_file_encoding="utf-8",
    )

    # Openai api key
    OPENAI_API_KEY :str = Field(
        description="OpenAI API Key",
    )

    # slack bot token
    SLACK_BOT_TOKEN:str = Field(
        description="Bot token for slack"
    )

    SLACK_APP_TOKEN :str = Field(
        description="App token of Socket model for slack"
    )

    # --------------------------------------------------
    # MongoDB Configuration (SAFE DEFAULTS)
    # --------------------------------------------------
    MONGODB_DATABASE_NAME: str = Field(
        default="slack_integration",
        description="MongoDB database name  .",
    )

    MONGODB_URI: str | None = Field(
        default="mongodb+srv://slackintegration:<dbpassword>@cluster0.z5ed8yy.mongodb.net/",
        description="MongoDB connection URI. If unset, local no-auth MongoDB is used.",
    )

    # Langsmith Configuration
    LANGCHAIN_TRACING_V2: bool = Field(
        description="Enable Langchain Tracing V2 if set to 'true'.",)
    
    LANGCHAIN_API_KEY:str = Field(
        description="Langchain API Key",
    )

    LANGCHAIN_PROJECT:str = Field(
        description="Langchain Project Name",
    )

    @field_validator(
    "OPENAI_API_KEY"
)
    @classmethod
    def check_required(cls, value: str, info) -> str:
        if not value or value.strip() == "":
            raise ValueError(f"{info.field_name} must be set and non-empty.")
        return value

    
try:
    settings = Settings()
    logger.info("Configuration loaded successfully.")
    os.environ["LANGCHAIN_TRACING_V2"] = str(settings.LANGCHAIN_TRACING_V2)
    os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    raise SystemExit(e)

