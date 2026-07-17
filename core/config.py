import os

from dotenv import load_dotenv

from core.logger import get_logger


logger = get_logger("ConfigManager")

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv(
        "PROJECT_NAME",
        "Enterprise Identity API",
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development",
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/identity_db",
    )

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "fallback-insecure-dev-key",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    )


settings = Settings()

logger.info("Configuration loaded successfully.")