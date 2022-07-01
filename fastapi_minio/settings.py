from pydantic import BaseSettings


class Settings(BaseSettings):
    minio_url: str
    minio_access_key: str
    minio_secret_key: str
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
