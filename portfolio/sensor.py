import os
from sqlalchemy import create_engine

USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_NAME = os.environ.get('POSTGRES_DB')

URL_CONNECT = f'postgresql://{USER}:{PASSWORD}@127.0.0.1:5432/{DB_NAME}'

engine = create_engine(URL_CONNECT)