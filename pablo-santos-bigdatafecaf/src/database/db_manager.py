import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class IotTemperatureDbManager:
    def __init__(self) -> None:
        self._engine = self.__create_connection_engine()
        self._session = self.__create_session_database()

    @property
    def get_engine(self):
        return self._engine

    @property
    def get_session(self):
        return self._session

    @property
    def get_all_properties(self):
        return (self._engine, self._session)

    def __create_connection_engine(self):
        USER = os.environ.get('POSTGRES_USER')
        PASSWORD = os.environ.get('POSTGRES_PASSWORD')
        DB_NAME = os.environ.get('POSTGRES_DB')
        URL = f'postgresql://{USER}:{PASSWORD}@localhost:5432/{DB_NAME}'

        return create_engine(URL)

    def __create_session_database(self):
        engine = self.__create_connection_engine()
        Session = sessionmaker(bind=engine)

        return Session()

    def __iter__(self):
        return iter((
            self.get_engine,
            self.get_session,
        ))
