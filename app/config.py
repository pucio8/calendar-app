import os
from pydantic import Field
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

# Path to the main project folder (e.g., /calnedar_app/)
PROJECT_ROOT = Path(__file__).parent.parent

class Settings(BaseSettings):
    """
    Class to manage the application configuration.
    Automatically loads variables from the .env file.
    """
    SECRET_KEY: str
    OAUTHLIB_INSECURE_TRANSPORT: str = "1"

    # --- Google API configuration ---
    GOOGLE_CREDENTIALS_PATH: Path = Field(default=PROJECT_ROOT / "credentials.json")
    
    GOOGLE_SCOPES: List[str] = Field(default=[
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ])
    
    # Missing variable - now added
    GOOGLE_REDIRECT_URI: str = Field(default="http://127.0.0.1:8000/auth/callback")

    class Config:
        env_file = PROJECT_ROOT / '.env'
        extra = 'ignore'

# Create a single, global instance of the settings
settings = Settings()

# Set the environment variable based on the loaded configuration
if settings.OAUTHLIB_INSECURE_TRANSPORT == "1":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
