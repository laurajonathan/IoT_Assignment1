import csv
from monitorAndNotify import Data
from monitorAndNotify import Database

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
            

def main():
    """
    Main Method
    """
    report = Report()
    report.check_status