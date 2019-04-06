"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is show data visualization

"""
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from monitorAndNotify import Database


class Analytics:
    """
    Analytics Class
    """

    def __init__(self):
        pass


def main():
    """
    Main Method
    """
    # Initialization
    database = Database()

    timestamp_list = []
    temp_list = []
    for temp, humid, timestamp in database.read_data():
        timestamp_list.append(timestamp.date())
        temp_list.append(temp)
    unique_date = sorted(set(timestamp_list))
    x = []
    y = []
    y_min = []
    y_max = []
    for date in unique_date:
        values = []
        for temp, timestamp in zip(temp_list, timestamp_list):
            if timestamp == date:
                values.append(temp)
        value = round(sum(values)/len(values), 1)
        value_min = round(min(values), 1)
        value_max = round(max(values), 1)
        x.append(date)
        y.append(value)
        y_min.append(value_min)
        y_max.append(value_max)
    
    plotly.offline.init_notebook_mode(connected=True)

    trace1 = go.Bar(
        x=x,
        y=y_min,
        name='Min'
    )
    trace2 = go.Bar(
        x=x,
        y=y_max,
        name='Max'
    )
    
    trace3 = go.Bar(
        x=x,
        y=y,
        name='Average'
    )
    
    data = [trace1, trace2, trace3]
    
    plotly.offline.plot({
        "data": data,
        "layout": go.Layout(title='Analytic', barmode='group')
    }, auto_open=True)
###############################################################################
    x = []
    y = []
    y2 = []
    for temp, humid, timestamp in database.read_data():
        x.append(timestamp)
        y.append(temp)
        y2.append(humid)
    plt.figure(figsize=(16,10))
    plt.plot(x, y, color='green')
    plt.plot(x, y2, color='orange')
    plt.axhline(y=20, color='r', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Range')
    plt.title('Line Graph')
    plt.legend(['Temperature', 'Humidity', 'Set Point'], loc='upper left')
    plt.show()
    plt.savefig('linegraph.png')

    # Clear all object
    del database

if __name__ == "__main__":
    main()
