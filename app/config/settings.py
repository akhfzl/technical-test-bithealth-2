from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    EMBED_DIM: int = 384
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "messy_documents"
    QDRANT_PORT: int = 6333

    class Config:
        env_file = ENV_FILE
        env_file_encoding = "utf-8"

settings = Settings()
