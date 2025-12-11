import os
from dotenv import load_dotenv


load_dotenv()

class Settings():
    # Core App config
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM/AI Config
    OLLAMA_URL: str = os.getenv("OLLAMA_URL")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME")
    LLM_MAX_TOKENS: int = os.getenv("LLM_MAX_TOKENS")
    LLM_TEMPERATURE: float = os.getenv("LLM_TEMPERATURE")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not present in environment variable.")
    if not JWT_SECRET:
        raise ValueError("JWT_SECRET is not present in environment variable.")
    if not OLLAMA_URL:
        raise ValueError("OLLAMA_URL is not present in environment variable.")


settings = Settings()