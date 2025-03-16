import matplotlib.pyplot as plt
from database.db_manager import IotTemperatureDbManager
from sqlalchemy import func
from database.model import IotTemperature
from database.db_manager import IotTemperatureDbManager


class GraphGenerator:
    def __get_avg_temperature_total(self, filter_by=None):
        iot_temperature_db_manager = IotTemperatureDbManager()
        session = iot_temperature_db_manager.get_session

        query_view_temperature = (
            session.query(
                IotTemperature.date,
                func.avg(IotTemperature.temperature)
            )
        )

        if filter_by == 'In':
            query_view_temperature = (
                query_view_temperature.filter_by(location=filter_by)
            )
        elif filter_by == 'Out':
            query_view_temperature = (
                query_view_temperature.filter_by(location=filter_by)
            )

        view_temperature = (
            query_view_temperature
            .group_by(IotTemperature.date)
            .order_by(IotTemperature.date)
            .all()
        )

        date = [row[0] for row in view_temperature]
        avg_temperatures = [row[1] for row in view_temperature]

        return (date, avg_temperatures)

    def build_graph(
        self,
        plt_title,
        path_title_png,
        filter_by=None,
        width=12,
        heigth=6,
        graph_type='bar',
        linestyle='-',
        color='b',
        label='Média de temperatura',
    ):

        plt.figure(figsize=(width, heigth))

        date, avg_temperatures = self.__get_avg_temperature_total(filter_by)

        if graph_type == 'bar':
            plt.bar(date, avg_temperatures)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
        elif graph_type == 'plot':
            plt.plot(
                date,
                avg_temperatures,
                linestyle=linestyle,
                color=color,
                label=label
            )
            plt.grid(True)

        plt.title(plt_title, fontsize=14)
        plt.xlabel('Data', fontsize=12)
        plt.ylabel('Temperatura Média (°C)', fontsize=12)

        plt.xticks(rotation=45)

        # Exibindo o gráfico
        plt.tight_layout()  # Ajusta o layout para não sobrepor elementos

        # Use para mostrar o gráfico no jupyter notebook
        # plt.show()

        # Use quando estiver executando pelo VsCode
        plt.savefig(f'./outputs/{path_title_png}-figure.png', format='png')
        plt.close()
