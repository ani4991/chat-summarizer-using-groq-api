from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# load environment variables from .env file explicitly
load_dotenv()

class Settings(BaseSettings):
    groq_api_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# instantiate settings, which will use the loaded environment variables
settings = Settings()

# optionally, you can access the API key directly if needed elsewhere
api_key = os.environ.get("GROQ_API_KEY")