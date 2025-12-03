import os
from dotenv import load_dotenv


load_dotenv()

class Settings():
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not present in environment variable.")
    if not JWT_SECRET:
        raise ValueError("JWT_SECRET is not present in environment variable.")


settings = Settings()