from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # --------------------------------------------------
    # Pydantic Settings Config
    # --------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # --------------------------------------------------
    # AWS Configuration (optional)
    # --------------------------------------------------
    AWS_ACCESS_KEY: str | None = Field(
        default=None,
        description="AWS access key for authentication.",
    )

    AWS_SECRET_KEY: str | None = Field(
        default=None,
        description="AWS secret key for authentication.",
    )

    AWS_DEFAULT_REGION: str = Field(
        default="us-east-1",
        description="AWS region for cloud services.",
    )

    AWS_S3_BUCKET_NAME: str = Field(
        default="support-public-data",
        description="S3 bucket for application data.",
    )

    # --------------------------------------------------
    # LLM Configuration (OPTIONAL by default)
    # --------------------------------------------------
    OPENAI_API_KEY: str | None = Field(
        default=None,
        description="OpenAI API key (required only if OpenAI models are used).",
    )

    GOOGLE_API_KEY: str | None = Field(
        default=None,
        description="Google Gemini API key (required only if Gemini models are used).",
    )

    # --------------------------------------------------
    # MongoDB Configuration (SAFE DEFAULTS)
    # --------------------------------------------------
    MONGODB_DATABASE_NAME: str = Field(
        default="slack_integration",
        description="MongoDB database name.",
    )

    MONGODB_URI: str | None = Field(
        default="mongodb+srv://slackintegration:uWmqfCfqgtIYXbQ6@cluster0.z5ed8yy.mongodb.net/",
        description="MongoDB connection URI. If unset, local no-auth MongoDB is used.",
    )


# --------------------------------------------------
# Load settings safely
# --------------------------------------------------
try:
    settings = Settings()
    logger.info("Configuration loaded successfully")

except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise SystemExit(e)

