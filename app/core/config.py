
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AccessFlow"
    log_level: str = "INFO"
    storage_backend: str = "local"  # later: "s3"
    storage_path: str = "./uploads"

    class Config:
        env_file = ".env"

settings = Settings()