import matplotlib.pyplot as plt
from database.db_manager import IotTemperatureDbManager
from sqlalchemy import func
from database.model import IotTemperature
from database.db_manager import IotTemperatureDbManager


class GraphGenerator:
    def get_avg_temperature_total(self, filter_by=None):
        iottemperaturedbmanager = IotTemperatureDbManager()
        session = iottemperaturedbmanager.get_session

        query_view_temperature_total = (
            session.query(
                IotTemperature.date,
                func.avg(IotTemperature.temp)
            )
        )

        if filter_by == 'In':
            query_view_temperature_total = (
                query_view_temperature_total.filter_by(location=filter_by)
            )
        elif filter_by == 'Out':
            query_view_temperature_total = (
                query_view_temperature_total.filter_by(location=filter_by)
            )

        view_temperature_total = (
            query_view_temperature_total
            .group_by(IotTemperature.date)
            .order_by(IotTemperature.date)
            .all()
        )

        date = [row[0] for row in view_temperature_total]
        avg_temperatures = [row[1] for row in view_temperature_total]

        return (date, avg_temperatures)

    def build_graph(
        self,
        plt_title,
        width=12,
        heigth=6,
        graph_type='bar',
        linestyle='-',
        color='b',
        label='Média de temperatura',
    ):

        plt.figure(figsize=(width, heigth))

        date, avg_temperatures = self.get_avg_temperature_total()

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

        # Mostra o gráfico
        plt.show()

        # Salva o gráfico como png
        # plt.savefig('figure_temperatures_total.png', format='png')
        # plt.close()
