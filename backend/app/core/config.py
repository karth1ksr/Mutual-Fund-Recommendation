from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mutual Fund Recommendation Engine"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    
    # SQL Implementation
    DB_USER: str = "zube-ai"
    DB_PASSWORD: str = "ZubeAi@123"
    DB_HOST: str = "103.73.189.206"
    DB_PORT: int = 3307
    DB_NAME: str = "zube_mutual_fund"
    
    # Mongo Implementation
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "mf_recommendations_db"

    # API Keys
    PERPLEXITY_API_KEY: str
    GEMINI_API_KEY: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        import urllib.parse
        quoted_password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{quoted_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
