from pathlib import Path

from pydantic import BaseSettings
from sqlalchemy import URL

BASE_DIR = Path(__name__).parent.parent


class Settings(BaseSettings):
    db_driver: str = "postgresql+asyncpg"
    db_name: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str

    debug: bool = False
    show_sql: bool = False

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    class Config:
        env_file = '.env'

settings = Settings()

