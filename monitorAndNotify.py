"""
monitorAndNotify.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to update the temperature and humidity every minutes.

"""

import datetime
import MySQLdb
from virtual_sense_hat import VirtualSenseHat


class Data:
    """Data class for reading the data from sense hat sensor"""

    def __init__(self, sense_hat):
        self.__sense_hat = sense_hat
        self.__temperature = 0
        self.__humidity = 0
        self.__timestamp = datetime.datetime.now()

    def read_data(self):
        self.__temperature = self.__sense_hat.get_temperature()
        self.__humidity = self.__sense_hat.get_humidity()
        self.__timestamp = datetime.datetime.now()

    def get_data(self):
        return self.__temperature, self.__humidity, self.__timestamp

    def __def__(self):
        pass


class Database:
    """Database class for all database operations"""

    def __init__(self):
        self.__connection = MySQLdb.connect(
            "localhost", "pi", "suwat513", "Assignment1")

    def __execute_query(self, query, *attributes):
        with self.__connection.cursor() as cursor:
            cursor.execute(query, attributes)
            result = cursor.fetchall()
        self.__connection.commit()
        return result

    def insert_data(self, *attributes):
        query = """
            INSERT INTO data (temp, humid, timestamp) VALUES (%s, %s, %s)
        """
        self.__execute_query(query, *attributes)
        return "Success!"

    def read_data(self):
        query = """
            SELECT temp, humid, timestamp FROM data
        """
        return self.__execute_query(query)

    def __del__(self):
        self.__connection.close()


def main():
    sense = VirtualSenseHat.getSenseHat()
    data = Data(sense)
    data.read_data()
    temp, humid, timestamp = data.get_data()
    database = Database()
    database.insert_data(temp, humid, timestamp)
    database.read_data()
    del data
    del database


if __name__ == "__main__":
    main()
