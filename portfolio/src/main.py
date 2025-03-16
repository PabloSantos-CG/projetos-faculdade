import pandas as pd
from sqlalchemy import Date, func
from database.model import IotTemperature
import matplotlib.pyplot as plt
from database.db_manager import IotTemperatureDbManager


PATH_DATA = './data/IOT-temp.csv'

iottemperaturedbmanager = IotTemperatureDbManager()
engine, session = iottemperaturedbmanager.get_all_properties

temperature_iot_df = pd.read_csv(PATH_DATA)

temperature_iot_df["noted_date"] = pd.to_datetime(
    temperature_iot_df["noted_date"].str.split(' ').str[0],
    format="%d-%m-%Y"
)

temperature_iot_df.columns = ['id', 'room_id', 'date', 'temperature', 'location']
# temperature_iot_df.to_sql(
#     'iot_temperatures',
#     engine,
#     if_exists='replace',
#     index=False,
#     dtype={
#         'date': Date
#     }
# )

# 1 - média da temperatura geral - gráfico em linha
temperatures_total = (
    session.query(
        IotTemperature.date,
        func.avg(IotTemperature.temp).label('Average')
    )
    .group_by(IotTemperature.date)
    .order_by(IotTemperature.date)
    .all()
)

date = [row[0] for row in temperatures_total]
avg_temperatures = [row[1] for row in temperatures_total]

# plt.figure(figsize=(12, 6))
plt.plot(date, avg_temperatures, linestyle='-', color='b', label= 'Média de temperatura')

plt.title('Média de Temperatura Geral', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Temperatura Média (°C)', fontsize=12)

plt.xticks(rotation=45)

# cria grade de linhas
plt.grid(True)

# Exibindo o gráfico
plt.tight_layout()  # Ajusta o layout para não sobrepor elementos
# plt.show()
plt.savefig('figure_temperatures_total.png', format='png')
plt.close()

# 2 - média da temperatura dentro da sala - gráfico barra
temperatures_in = (
    session.query(
        IotTemperature.date,
        func.avg(IotTemperature.temp).label('Average')
    )
    .filter_by(location='In')
    .group_by(IotTemperature.date)
    .order_by(IotTemperature.date)
    .all()
)

date_in = [row[0] for row in temperatures_in]
avg_temperatures_in = [row[1] for row in temperatures_in]

# plt.figure(figsize=(12, 6))
plt.bar(date_in, avg_temperatures_in)

plt.title('Média de Temperatura dentro da sala', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Temperatura Média (°C)', fontsize=12)

plt.xticks(rotation=45)

# cria grade de linhas
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Exibindo o gráfico
plt.tight_layout()  # Ajusta o layout para não sobrepor elementos
# plt.show()
plt.savefig('figure_temperatures_in_room.png', format='png')
plt.close()

# 3 - média da temperatura fora da sala - gráfico barra
temperatures_out = (
    session.query(
        IotTemperature.date,
        func.avg(IotTemperature.temp).label('Average')
    )
    .filter_by(location='Out')
    .group_by(IotTemperature.date)
    .order_by(IotTemperature.date)
    .all()
)

date_out = [row[0] for row in temperatures_out]
avg_temperatures_out = [row[1] for row in temperatures_out]

# plt.figure(figsize=(12, 6))
plt.bar(date_out, avg_temperatures_out)

plt.title('Média de Temperatura dentro da sala', fontsize=14)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Temperatura Média (°C)', fontsize=12)

plt.xticks(rotation=45)

# cria grade de linhas
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adicionando legenda
# plt.legend()

# Exibindo o gráfico
plt.tight_layout()  # Ajusta o layout para não sobrepor elementos
# plt.show()
plt.savefig('figure_temperatures_out_room.png', format='png')
plt.close()