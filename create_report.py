"""
createReport.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to create a simple report with csv format

"""

import re
import csv
from monitor_and_notify import Data
from monitor_and_notify import Database

REPORT_NAME = "report.csv"


class Report:
    """
    Report class for creating report
    """

    def __init__(self, data):
        self.__data = data
        self.__report_data = []

    def generate_status(self, temp, humid):
        """
        Generate status of temperature and humidity
        """
        temp_min, temp_max, humid_min, humid_max = self.__data.read_config()

        if not self.__data.data_out_of_range(temp, humid):
            status = "OK"
        else:
            status = "BAD:"
            if temp < temp_min:
                status += " %s *C below minimum temperature" \
                    % self.__data.diff(temp, temp_min)
            elif temp > temp_max:
                status += " %s *C over maximum temperature" \
                    % self.__data.diff(temp, temp_max)
            if humid < humid_min:
                if status[-1] != ":":
                    status += " and"
                status += " %s %% below minimum humidity" \
                    % self.__data.diff(humid, humid_min)
            elif humid > humid_max:
                if status[-1] != ":":
                    status += " and"
                status += " %s %% over maximum humidity" \
                    % self.__data.diff(humid, humid_max)
        return status

    def save_report_data(self, report_data):
        """
        Store report_data inside a private variable __report_data
        """
        self.__report_data = report_data

    def to_csv(self, report_name=REPORT_NAME):
        """
        Write data to csv file
        """
        with open(report_name, "w", newline='') as report:
            writer = csv.writer(report, delimiter=',', quoting=csv.QUOTE_ALL)
            header = ['Date', 'Status']
            writer.writerow(header)
            for data in self.__report_data:
                writer.writerow(data)
        report.close()


def main():
    """
    Main Method
    """
    # Initialization
    data = Data()
    database = Database()
    report = Report(data)

    print("Generating Report...")
    # Generate Report data
    report_data = []
    for temp, humid, timestamp in database.read_data():
        # Get status
        status = report.generate_status(temp, humid)
        # Set data in each row
        row = [timestamp.strftime('%d/%m/%Y'), status]
        # Append row
        report_data.append(row)

    # Save report data
    report.save_report_data(report_data)

    # Ask for user input
    report_name = input("Input report name(empty to use default name): ")

    # File name validation with regex
    pattern = re.compile(r"[\w]+(.csv)$")
    # Write to csv
    if pattern.match(report_name):
        report.to_csv(report_name)
    else:
        report.to_csv()

    # Clear all object
    del data
    del database
    del report


if __name__ == "__main__":
    main()
