"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is show data visualization

"""
import plotly
from plotly.offline import plot
import plotly.graph_objs as go
from monitorAndNotify import Database
import numpy as np


class Analytics:
    """
    Analytics Class
    """


def main():
    """
    Main Method
    """
    # Initialization
    database = Database()
    x = []
    y = []
    for temp, humid, timestamp in database.read_data():
        x.append(timestamp)
        y.append(temp)
    plotly.offline.init_notebook_mode(connected=True)
    #x = np.random.randn(500)
    data = [go.Histogram(x=y)]
    plotly.offline.plot({
        "data": data,
        "layout": go.Layout(title="hello world")
    }, auto_open=True)

    # Clear all object
    del database


if __name__ == "__main__":
    main()
