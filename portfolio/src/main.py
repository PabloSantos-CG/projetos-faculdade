import pandas as pd
from sqlalchemy import Date
from database.db_manager import IotTemperatureDbManager


PATH_DATA = './data/IOT-temp.csv'

iottemperaturedbmanager = IotTemperatureDbManager()
engine, session = iottemperaturedbmanager.get_all_properties

temperature_iot_df = pd.read_csv(PATH_DATA)

temperature_iot_df["noted_date"] = pd.to_datetime(
    temperature_iot_df["noted_date"].str.split(' ').str[0],
    format="%d-%m-%Y"
)

temperature_iot_df.columns = [
    'id', 'room_id', 'date', 'temperature','location'
]

temperature_iot_df.to_sql(
    'iot_temperatures',
    engine,
    if_exists='replace',
    index=False,
    dtype={
        'date': Date
    }
)

# 1 - média da temperatura geral - gráfico em linha


# 2 - média da temperatura dentro da sala - gráfico barra


# 3 - média da temperatura fora da sala - gráfico barra
