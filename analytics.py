"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is for data visualization

"""

from abc import ABC, abstractmethod
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from monitor_and_notify import Data
from monitor_and_notify import Database


class Graph(ABC):
    """
    Generate graph Class
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def data_preprocessing(self, data_from_db, config):
        """
        Data preprocessing or preparation before ploting the graph
        """

    @abstractmethod
    def generate_graph(self):
        """
        Draw a graph
        """


class LineGraph(Graph):
    """
    LineGraph Class
    """

    def __init__(self):
        super(LineGraph, self).__init__()
        self.__temp = []
        self.__humid = []
        self.__timestamp = []
        self.__temp_min = 0
        self.__temp_max = 0
        self.__humid_min = 0
        self.__humid_max = 0

    def data_preprocessing(self, data_from_db, config):
        # Set data from database
        for temp, humid, timestamp in data_from_db:
            self.__temp.append(temp)
            self.__humid.append(humid)
            self.__timestamp.append(timestamp)

        # Set data from config
        self.__temp_min = config[0]
        self.__temp_max = config[1]
        self.__humid_min = config[2]
        self.__humid_max = config[3]

    def generate_graph(self):
        # Initialize graph
        fig, ax1 = plt.subplots(figsize=(16, 10))

        # Plot temperature and temp config
        ax1.plot(self.__timestamp, self.__temp, color='green')
        ax1.axhline(y=self.__temp_min, color='green', linestyle=':')
        ax1.axhline(y=self.__temp_max, color='green', linestyle=':')

        ax1.set_xlabel('Datetime')

        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Temperature (*C)', color='green')
        ax1.tick_params('y', colors='green')

        # Plot humidity and humid config
        ax2 = ax1.twinx()
        ax2.plot(self.__timestamp, self.__humid, color='orange')
        ax1.axhline(y=self.__humid_min, color='orange', linestyle='--')
        ax1.axhline(y=self.__humid_max, color='orange', linestyle='--')
        ax2.set_ylabel('Humidity (%)', color='orange')
        ax2.tick_params('y', colors='orange')

        plt.title('Analytics')

        fig.tight_layout()

        # Save to png
        plt.savefig('line_graph.png')
        plt.close()


class BarGraph(Graph):
    """
    BarGraph Class
    """

    def __init__(self):
        super(BarGraph, self).__init__()
        self.__temp_min = []
        self.__temp_avg = []
        self.__temp_max = []
        self.__humid_min = []
        self.__humid_avg = []
        self.__humid_max = []
        self.__timestamp = []

    @classmethod
    def __cal_min_max_avg(cls, value):
        value_avg = round(sum(value)/len(value), 1)
        value_min = round(min(value), 1)
        value_max = round(max(value), 1)
        return value_min, value_avg, value_max

    def data_preprocessing(self, data_from_db, config):
        # Get timestamp date from data
        _timestamp = [timestamp.date() for _, _, timestamp in data_from_db]

        # Get unique date and sort data
        _unique_date = sorted(set(_timestamp))

        # Run the calculation for temp and humid
        for date in _unique_date:
            _temp = []
            _humid = []
            # Get data for each match date
            for temp, humid, timestamp in data_from_db:
                timestamp = timestamp.date()
                if timestamp == date:
                    _temp.append(temp)
                    _humid.append(humid)

            # Calculate min max avg
            temp_value = self.__cal_min_max_avg(_temp)
            humid_value = self.__cal_min_max_avg(_humid)

            # Append calculated data to list
            self.__temp_min.append(temp_value[0])
            self.__temp_avg.append(temp_value[1])
            self.__temp_max.append(temp_value[2])
            self.__humid_min.append(humid_value[0])
            self.__humid_avg.append(humid_value[1])
            self.__humid_max.append(humid_value[2])

        # Set timestamp as unique date
        self.__timestamp = _unique_date

    def generate_graph(self):
        # Initialize each bar of temperature bar graph
        bar_min = go.Bar(
            x=self.__timestamp,
            y=self.__temp_min,
            name='Min',
            marker=dict(
                color='rgb(0,0,255)'
            )
        )
        bar_avg = go.Bar(
            x=self.__timestamp,
            y=self.__temp_avg,
            name='Average',
            marker=dict(
                color='rgb(0,255,0)'
            )
        )
        bar_max = go.Bar(
            x=self.__timestamp,
            y=self.__temp_max,
            name='Max',
            marker=dict(
                color='rgb(255,0,0)'
            )
        )

        # Set data to plot
        data = [bar_min, bar_avg, bar_max]

        # Plot the temperature graph with offline mode
        plotly.offline.plot({
            "data": data,
            "layout": go.Layout(
                title='Temperature',
                barmode='group',
                xaxis={'title': 'Datetime'},
                yaxis={'title': 'Temperature (*C)'}
            )
        }, auto_open=False, filename="bar_temp.html")

        # Initialize each bar of humidity bar graph
        bar_min = go.Bar(
            x=self.__timestamp,
            y=self.__humid_min,
            name='Min',
            marker=dict(
                color='rgb(0,0,255)'
            )
        )
        bar_avg = go.Bar(
            x=self.__timestamp,
            y=self.__humid_avg,
            name='Average',
            marker=dict(
                color='rgb(0,255,0)'
            )
        )
        bar_max = go.Bar(
            x=self.__timestamp,
            y=self.__humid_max,
            name='Max',
            marker=dict(
                color='rgb(255,0,0)'
            )
        )

        # Set data to plot
        data = [bar_min, bar_avg, bar_max]

        # Plot the humidity graph with offline mode
        plotly.offline.plot({
            "data": data,
            "layout": go.Layout(
                title='Humidity',
                barmode='group',
                xaxis={'title': 'Datetime'},
                yaxis={'title': 'Humidity (%)'}
            )
        }, auto_open=False, filename="bar_humid.html")


def main():
    """
    Main Method
    """
    # Initialization
    data = Data()
    database = Database()
    bar_graph = BarGraph()
    line_graph = LineGraph()

    # Read data from database
    data_from_db = database.read_data()
    # Read config from config_file
    config = data.read_config()

    # Bar Graph
    bar_graph.data_preprocessing(data_from_db, config)
    bar_graph.generate_graph()

    # Line Graph
    line_graph.data_preprocessing(data_from_db, config)
    line_graph.generate_graph()

    # Clear all object
    del data
    del database
    del bar_graph
    del line_graph


if __name__ == "__main__":
    main()
