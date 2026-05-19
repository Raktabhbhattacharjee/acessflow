from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "AccessFlow"
    log_level: str = "INFO"

    storage_backend: str = "local"
    storage_path: str = "./uploads"

    aws_region: str = "ap-south-1"
    s3_bucket_name: str | None = None


settings = Settings()