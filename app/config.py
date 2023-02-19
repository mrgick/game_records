from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    app_title: str = "Record of game matches"
    app_description: str = "Api for an app that keeps records of game matches"
    app_version: str = "0.0.1"
    db_url: PostgresDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
