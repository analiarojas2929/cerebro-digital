from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Cerebro Digital"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-secret-key-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://cerebro:cerebro123@localhost:5432/cerebro_digital"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Vector Database
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    # Neural Models
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    CLASSIFIER_MODEL: str = "distilbert-base-uncased"
    
    # Memory Settings
    SHORT_TERM_MEMORY_SIZE: int = 50
    LONG_TERM_MEMORY_THRESHOLD: float = 0.75
    MAX_CONTEXT_LENGTH: int = 2000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
