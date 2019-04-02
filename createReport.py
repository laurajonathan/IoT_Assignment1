"""
createReport.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to create csv file

"""

import csv
from monitorAndNotify import Data
from monitorAndNotify import Database
<<<<<<< HEAD
from virtual_sense_hat import VirtualSenseHat

CONFIG_FILE = "config.json"

class CSV(object):
    """
    CSV class for writing csv file containing date and status
    """

    def __init__(self, data):
        self.__data = data

    def set_status(self, temp, humid):
        """
        Set status on the temperature and humidity
        """
        temp_min, temp_max, humid_min, humid_max = self.__data.read_config()

        if self.__data.data_out_of_range(temp, humid):
            status = "OK"
        else:
            if temp < temp_min:
                status = "BAD: %s below minimum temperature" %round((temp_min-temp), 1)
            if temp > temp_max:
                status = "BAD: %s over maximum temperature" %round((temp-temp_max), 1)
            if temp < humid_min:
                status = "BAD: %s below minimum humidity" %round((humid_min-humid), 1)
            if temp < humid_max:
                status = "BAD: %s over maximum humidity" %round((humid-humid_max), 1)
        return status

    def create_csvfile(self, csv_data):
        """
        Create csvfile
        """
        with open("report.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
            header = ['Date', 'Status']
            writer.writerow(header)
            for data in csv_data:
                writer.writerow(data)
        csvfile.close()

    def format_date(self, date):
        """
        Formatting date to dd/mm/yy
        """
        date = date.strftime('%d/%m/%Y')
        return date
=======

class Report:
    """Report class for creating csv file from database"""
    database = Database()
    temp, humid, timestamp = database.read_data()

    def __init__(self):
        self.__dataread = self.database.read_data()
        #self.__dataread = 21.0, 50.0, datetime.datetime.now()

    def check_status(self):
        self.__status = status
        for d in __dataread:
            print(d)
            
>>>>>>> master

def main():
    """
    Main Method
    """
<<<<<<< HEAD
    database = Database()
    sense = VirtualSenseHat.getSenseHat()
    data = Data(sense, CONFIG_FILE)
    csv_report = CSV(data)

    result = []
    for temp_data in database.read_data():
        result.append([temp_data[0], temp_data[1], temp_data[2]])

    csv_data = []
    print result

    for temp_result in result:
        date = temp_result[2]
        format_date = csv_report.format_date(date)
        #print(format_date)

        temp = temp_result[0]
        humid = temp_result[1]
        setting_status = csv_report.set_status(temp, humid)
        #print(setting_status)

        csv_data.append([format_date, setting_status])
        print csv_data

    csv_report.create_csvfile(csv_data)

if __name__ == "__main__":
    main()
=======
    report = Report()
    report.check_status
>>>>>>> master
