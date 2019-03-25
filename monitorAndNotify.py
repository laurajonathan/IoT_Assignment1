"""
monitorAndNotify.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to update the temperature and humidity every minutes.

"""

import datetime
import MySQLdb
from virtual_sense_hat import VirtualSenseHat


class Data:
    """Data class for reading the data from sense hat sensor
    """

    def __init__(self, sense_hat):
        self._sense_hat = sense_hat
        self._temperature = 0
        self._humidity = 0
        self._timestamp = datetime.datetime.now()

    def read_data(self):
        self._temperature = self._sense_hat.get_temperature()
        self._humidity = self._sense_hat.get_humidity()
        self._timestamp = datetime.datetime.now()

    def get_data(self):
        return self._temperature, self._humidity, self._timestamp


def connect_to_database():
    return MySQLdb.connect("localhost", "root", "suwat513", "Assignment1")


def insert_data_into_database(temp, humid, timestamp):
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("""
                       INSERT INTO data (temp, humid, timestamp)
                       VALUES (%s, %s, %s)""",
                       (temp, humid, timestamp))
    connection.commit()
    connection.close()


def read_data_from_database():
    connection = connect_to_database()
    with connection.cursor() as cursor:
        cursor.execute("SELECT temp, humid, timestamp FROM data")
        print("{:15} {:15} {:15}".format("Temp", "Humid", "Timestamp"))
        print("===========================================================")

        for reading in cursor.fetchall():
            print("{:15} {:15} {:15}".format(
                str(reading[0]),
                str(reading[1]),
                str(reading[2])))

    connection.close()


def main():
    sense = VirtualSenseHat.getSenseHat()
    data = Data(sense)
    data.read_data()
    temp, humid, timestamp = data.get_data()
    insert_data_into_database(temp, humid, timestamp)
    read_data_from_database()


if __name__ == "__main__":
    main()
