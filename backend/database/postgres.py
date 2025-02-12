from sqlalchemy import Engine, create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv, find_dotenv
from typing import Tuple

from sqlalchemy.orm import Session, sessionmaker


def get_environment_variables() -> Tuple[str, str, str, str]:
    if "AWS_EXECUTION_ENV" not in os.environ:
        load_dotenv(find_dotenv())

    username = os.getenv("USERNAME_POSTGRES")
    password = os.getenv("PASSWORD_POSTGRES")
    host = os.getenv("HOST_POSTGRES")
    database = os.getenv("DATABASE_POSTGRES")

    return username, password, host, database


class Postgres:
    def __init__(self, username: str, password: str, host: str, database: str):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.engine = self.start_engine()
        self.session_maker = self.start_session()

    def start_engine(self) -> Engine:
        database_url = f"postgresql+pg8000://{self.username}:%s@{self.host}/{self.database}?application_name=microsservico"
        return create_engine(database_url % quote_plus(self.password), echo=True)

    def start_session(self) -> sessionmaker[Session]:
        return sessionmaker(
            bind=self.engine, autocommit=False, expire_on_commit=False, autoflush=False
        )

    def get_engine(self) -> Engine:
        return self.engine

    def get_session(self) -> Session:
        return self.session_maker()


POSTGRES_INSTANCE = Postgres(*get_environment_variables())


def get_db() -> Session:
    db = POSTGRES_INSTANCE.get_session()
    try:
        yield db
    finally:
        db.close()
