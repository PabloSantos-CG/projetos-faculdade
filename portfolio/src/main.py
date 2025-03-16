import pandas as pd
from sqlalchemy import Date
from database.db_manager import IotTemperatureDbManager
from utils.graph_generator import GraphGenerator


PATH_DATA = './data/IOT-temp.csv'

# Gera uma instância do gerenciador de Banco de dados e realiza configurações
iot_temperature_db_manager = IotTemperatureDbManager()
engine, session = iot_temperature_db_manager.get_all_properties

# Cria dataframe do csv
temperature_iot_df = pd.read_csv(PATH_DATA)

# Formata a coluna de datas
temperature_iot_df["noted_date"] = pd.to_datetime(
    temperature_iot_df["noted_date"].str.split(' ').str[0],
    format="%d-%m-%Y"
)

# Renomeia as colunas do dataframe
temperature_iot_df.columns = [
    'id', 'room_id', 'date', 'temperature', 'location'
]

# Popula o banco de dados com os dados do dataframe
temperature_iot_df.to_sql(
    'iot_temperatures',
    engine,
    if_exists='replace',
    index=False,
    dtype={
        'date': Date
    }
)

# VIEWS com o SqlAlchemy ORM
graph_generator = GraphGenerator()

# 1 - Média da temperatura geral - gráfico em linha
graph_generator.build_graph(
    plt_title='Média de Temperatura Geral',
    graph_type='plot',
    title_png_for_save='avg-total'
)

# 2 - média da temperatura dentro da sala - gráfico barra
graph_generator.build_graph(
    plt_title='Média de Temperatura dentro da sala',
    filter_by='In',
    title_png_for_save='avg-in-room'
)

# 3 - média da temperatura fora da sala - gráfico barra
graph_generator.build_graph(
    plt_title='Média de Temperatura fora da sala',
    filter_by='Out',
    title_png_for_save='avg-out-room'
)
