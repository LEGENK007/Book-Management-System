import os
from dotenv import load_dotenv


load_dotenv()

class Settings():
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not present in environment variable.")


settings = Settings()