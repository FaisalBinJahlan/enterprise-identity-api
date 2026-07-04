import os
from dotenv import load_dotenv
from core.logger import get_logger

# Initialize logger for configuration events
logger = get_logger("ConfigManager")

# Load environment variables from the .env file into the system
load_dotenv()

class Settings:
    """
    Centralized configuration manager.
    Reads sensitive data from environment variables to prevent hardcoding secrets.
    """
    PROJECT_NAME: str = "Enterprise Identity API"
    VERSION: str = "1.0.0"
    
    # Fetch the secret key, with a fallback ONLY for local debugging
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-insecure-dev-key")

# Instantiate the settings object to be imported across the application
settings = Settings()

logger.info(f"{settings.PROJECT_NAME} configurations loaded successfully.")