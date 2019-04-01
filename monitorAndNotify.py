"""
monitorAndNotify.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to update the temperature and humidity every minutes.

"""

import datetime
import requests
import json
import MySQLdb
from virtual_sense_hat import VirtualSenseHat

CONFIG_FILE = "config.json"
API_KEY = "o.cYDH4cl2j2C1DA5Wxt4vPZi4pS7eMR9V"
MAX_NOTIFICATION_PER_DAY = 1


class Data:
    """Data class for reading the data from sense hat sensor"""

    def __init__(self, sense_hat):
        self.__sense_hat = sense_hat
        self.__temperature = 0
        self.__humidity = 0
        self.__timestamp = datetime.datetime.now()

    def read_data(self):
        """
        Read the temperature and humidity from sense hat sensor
        with current timestamp
        """
        self.__temperature = self.__sense_hat.get_temperature()
        self.__humidity = self.__sense_hat.get_humidity()
        self.__timestamp = datetime.datetime.now()

    def get_data(self):
        """
        Return the data with format: temp, humid, timestamp
        """
        return self.__temperature, self.__humidity, self.__timestamp

    def __def__(self):
        pass


class Database:
    """Database class for all database operations"""

    def __init__(self):
        self.__connection = MySQLdb.connect(
            "localhost", "root", "suwat513", "Assignment1")

    def __execute_query(self, query, *attributes):
        """Execute query"""
        with self.__connection.cursor() as cursor:
            cursor.execute(query, attributes)
            result = cursor.fetchall()
        self.__connection.commit()
        return result

    @classmethod
    def __validate_data(cls, *attributes):
        """Validate the type of the data before insert into database"""
        for attr in attributes[:-1]:
            if not isinstance(attr, float):
                return False
        if not isinstance(attributes[-1], datetime.datetime):
            return False
        return True

    def insert_data(self, *attributes):
        """
        Validate the data and prevent SQL Injection attack with
        parametrised query then insert data into database
        """
        query = """
            INSERT INTO data (temp, humid, timestamp) VALUES (%s, %s, %s)
        """
        if self.__validate_data(*attributes):
            self.__execute_query(query, *attributes)

    def read_data(self):
        """
        Read data from the database with pre-defined query
        """
        query = """
            SELECT temp, humid, timestamp FROM data
        """
        return self.__execute_query(query)

    @classmethod
    def __validate_notification(cls, *attributes):
        """Validate the type of the notification before insert into database"""
        for attr in attributes[:-1]:
            if not isinstance(attr, str):
                return False
        if not isinstance(attributes[-1], datetime.datetime):
            return False
        return True

    def insert_notification(self, *attributes):
        """
        Validate the notification and prevent SQL Injection attack with
        parametrised query then insert notification into database
        """
        query = """
            INSERT INTO notification (title, body, timestamp)
            VALUES (%s, %s, %s)
        """
        if self.__validate_notification(*attributes):
            self.__execute_query(query, *attributes)

    def read_notification(self, max_notification_per_day):
        """
        Read notification from the database with pre-defined query
        and return False if the max_notification_per_day reached
        """
        query = """
            SELECT timestamp FROM notification
        """
        result = self.__execute_query(query)
        today = datetime.datetime.today().date()
        count = 0
        for _r in result:
            if _r[0].date() == today:
                count += 1
        if count >= max_notification_per_day:
            return False
        return True

    def __del__(self):
        self.__connection.close()


class Notification:
    """Notify user via Pushbullet if the data is out of config_file range"""

    def __init__(self, access_token):
        self.__access_token = access_token

    def read_config(self, config_file):
        """
        Read config data from config file
        """
        with open(config_file) as json_file:
            self.__config = json.load(json_file)

    def send_notification_via_pushbullet(self, title, body):
        """ Sending notification via pushbullet.
            Args:
                title (str) : title of text.
                body (str) : Body of text.
        """
        data_send = {
            "type": "note",
            "title": title,
            "body": body
        }
        resp = requests.post(
            "https://api.pushbullet.com/v2/pushes",
            data=json.dumps(data_send),
            headers={
                "Authorization": "Bearer " + self.__access_token,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code != 200:
            raise Exception("Something wrong")
        else:
            print("complete sending")


def main():
    """
    Main Method
    """
    sense = VirtualSenseHat.getSenseHat()
    data = Data(sense)
    data.read_data()
    temp, humid, timestamp = data.get_data()
    database = Database()
    database.insert_data(temp, humid, timestamp)
    database.read_data()
    #database.insert_notification("title test", "body test", datetime.datetime.now())
    print(database.read_notification(2))
    del data
    del database


if __name__ == "__main__":
    main()
