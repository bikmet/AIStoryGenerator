#takes in all environment variables from .env and map them into Python objects (to use in our code)

from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_PREFIX: str = '/api'
    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: str = ""

    OPENAI_API_KEY: str

    CLOUDFLARE_ACCOUNT_ID: str
    CLOUDFLARE_API_TOKEN: str

    #since ALLOWED_ORIGINS url are split by a comma, store them in a list
    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v:str) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return []

    #set the configuration to correctly load the .env file
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings() #constructor