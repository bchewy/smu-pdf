from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_REQUESTS_PER_HOUR: int = 10
    ALLOWED_HOSTS: list = ["localhost:5000"]
    
    class Config:
        env_file = ".env"

settings = Settings() 