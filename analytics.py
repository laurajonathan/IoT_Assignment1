"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is show data visualization

"""
import matplotlib.pyplot as plt

from monitorAndNotify import Data
from monitorAndNotify import Database

class Analytics:
    """
    Analytics class for visualize data obtained from the sensehat
    """

    def __init__(self):
        pass
    
    def generate_linegraph(self, temp, humid, date):
        """
        Generate linegraph of temperature and humidity
        """
        plt.plot(date, temp, color='g')
        plt.plot(date, humid, color='orange')
        plt.xlabel('Date')
        plt.ylabel('Range')
        plt.title('Line Graph')
        plt.legend(['Green = Temperature', 'Orange = Humidity'], loc='upper left')
        plt.show()

def main():
        """
        Main Method
        """

        # Initialization
        data = Data()
        database = Database()

        # Get the data from the database
        #obtained_data = database.read_data()

        # Extract temperature, humidity and timestamp from database
        obtained_data = []
        
        for temp, humid, timestamp in database.read_data():
            date = timestamp.strftime('%d/%m/%Y')
            formatted_data = [[temp], [humid], [date]]
            obtained_data.append(formatted_data)
        print(obtained_data)
        
        #analytics = Analytics()
        #analytics = analytics.generate_linegraph()        


if __name__ == "__main__":
    main()
