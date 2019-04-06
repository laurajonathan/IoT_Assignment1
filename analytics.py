"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is show data visualization

"""
import plotly
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from monitorAndNotify import Database

class Graph:
    """
    Generate graph Class
    """
    def __init__(self):
        pass

    def generate_graph(self):
        pass

class LineGraph(Graph):
    """
    LineGraph Class
    """

    def __init__(self):
        pass

    def generate_graph(self, x, y, y2):
        fig, ax1 = plt.subplots(figsize=(16,10))
        ax1.plot(x, y, color='green')
        ax1.axhline(y=20, color='green', linestyle=':')
        ax1.axhline(y=50, color='green', linestyle=':')
        ax1.set_xlabel('Datetime')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel('Temperature (*C)', color='green')
        ax1.tick_params('y', colors='green')
        
        ax2 = ax1.twinx()
        ax2.plot(x, y2, color='orange')
        ax1.axhline(y=30, color='orange', linestyle='--')
        ax1.axhline(y=60, color='orange', linestyle='--')
        ax2.set_ylabel('Humidity (%)', color='orange')
        ax2.tick_params('y', colors='orange')
        
        plt.title('Line Graph')
        
        fig.tight_layout()
        plt.show()
        plt.savefig('linegraph.png')
    
class BarGraph(Graph):
    """
    BarGraph Class
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
    y_avg = []
    y_min = []
    y_max = []
    for date in unique_date:
        values = []
        for temp, timestamp in zip(temp_list, timestamp_list):
            if timestamp == date:
                values.append(temp)
        value_avg = round(sum(values)/len(values), 1)
        value_min = round(min(values), 1)
        value_max = round(max(values), 1)
        x.append(date)
        y_avg.append(value_avg)
        y_min.append(value_min)
        y_max.append(value_max)
    
    #plotly.offline.init_notebook_mode(connected=True)

    bar_min = go.Bar(
        x=x,
        y=y_min,
        name='Min',
        marker=dict(
            color='rgb(0,0,255)'
        )
    )
    bar_avg = go.Bar(
        x=x,
        y=y_avg,
        name='Average',
        marker=dict(
            color='rgb(0,255,0)'
        )
    )
    
    bar_max = go.Bar(
        x=x,
        y=y_max,
        name='Max',
        marker=dict(
            color='rgb(255,0,0)'
        )
    )
    
    data = [bar_min, bar_avg, bar_max]
    
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

    line_graph = LineGraph()
    line_graph.generate_graph(x,y,y2)
    
    # Clear all object
    del database

if __name__ == "__main__":
    main()
