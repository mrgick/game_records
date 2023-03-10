from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_title: str = "Records of game matches"
    app_description: str = "Api for an app that keeps records of game matches"
    app_version: str = "0.0.1"
    static_path: Path = Path().absolute() / 'app' / 'static'
    templates_path: Path = Path().absolute() / 'app' / 'templates'
    db_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
