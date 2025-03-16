from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IotTemperature(Base):
    __tablename__ = 'iot_temperatures'

    id = Column(String, primary_key=True)
    room_id = Column(String)
    date = Column(Date)
    temp = Column(String)
    location = Column(String)
