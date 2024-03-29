"""
monitor_and_notify.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to update the temperature and humidity every minutes.

"""

import datetime
import json
import requests
import MySQLdb
from virtual_sense_hat import VirtualSenseHat

API_KEY = "o.cYDH4cl2j2C1DA5Wxt4vPZi4pS7eMR9V"
CONFIG_FILE = "config.json"
MAX_BAD_ITEM = 2
MAX_NOTIFICATION_PER_DAY = 1
TITLE = "Send from Raspberry Pi! (Data Out Of Range)"


class Data:
    """
    Data class for reading the data from sense hat sensor and
    read the config file for the valid range in each type of data
    """

    def __init__(self,
                 sense_hat=VirtualSenseHat.get_sense_hat(),
                 config_file=CONFIG_FILE):
        with open(config_file) as json_file:
            self.__config = json.load(json_file)
        self.__sense_hat = sense_hat
        self.__temp_min = self.__config['min_temperature']
        self.__temp_max = self.__config['max_tempetature']
        self.__humid_min = self.__config['min_humidity']
        self.__humid_max = self.__config['max_humidity']

    def read_data(self):
        """
        Read the temperature and humidity from sense hat sensor
        with current timestamp
        """
        return (
            self.__sense_hat.get_temperature(),
            self.__sense_hat.get_humidity(),
            datetime.datetime.now()
        )

    def read_config(self):
        """
        Read the config
        """
        return (
            self.__temp_min,
            self.__temp_max,
            self.__humid_min,
            self.__humid_max
        )

    def data_out_of_range(self, temp, humid):
        """
        Check if temp and humid is out of the valid data range
        """
        if (temp < self.__temp_min
                or temp > self.__temp_max
                or humid < self.__humid_min
                or humid > self.__humid_max):
            return True
        return False

    @classmethod
    def diff(cls, data, config):
        """
        Return difference between two data with 1 decimal places
        """
        return round(abs(data - config), 1)

    def cal_out_of_range(self, temp, humid):
        """
        Calculate the difference if the data is out of range
        else return 0
        """
        diff = 0
        if temp < self.__temp_min:
            diff += self.diff(temp, self.__temp_min)
        elif temp > self.__temp_max:
            diff += self.diff(temp, self.__temp_max)
        if humid < self.__humid_min:
            diff += self.diff(humid, self.__humid_min)
        elif humid > self.__humid_max:
            diff += self.diff(humid, self.__humid_max)
        return diff


class Database:
    """
    Database class for all database operations
    """

    def __init__(self):
        self.__connection = MySQLdb.connect(
            "localhost", "pi", "suwat513", "Assignment1"
        )

    def __execute_query(self, query, *attributes):
        """
        Execute query
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query, attributes)
            result = cursor.fetchall()
        self.__connection.commit()
        return result

    @classmethod
    def __validate_data(cls, *attributes):
        """
        Validate the type of the data before insert into database
        """
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

    def read_data(self, today=False):
        """
        Read data from the database with pre-defined query
        If today is True read the data with timestamp = today
        else read all data
        """
        if today:
            query = """
                SELECT temp, humid, timestamp
                FROM data
                WHERE timestamp >= CURDATE()
            """
        else:
            query = """
                SELECT temp, humid, timestamp FROM data
            """
        return self.__execute_query(query)

    @classmethod
    def __validate_notification(cls, *attributes):
        """
        Validate the type of the notification before insert into database
        """
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
    """
    Notify user via Pushbullet if the data is out of config_file range
    """

    def __init__(self, access_token=API_KEY):
        self.__access_token = access_token
        self.__title = "Default Title"
        self.__body = "Default Body"

    def set_message(self, data, *config, title=TITLE):
        """
        Setter for the title and body of the message for notification
        if the config data is included reply temp and humid with config
        else reply temp and humid
        """
        self.__title = title
        if config:
            self.__body = """
                Valid data in setting is:\n
                    temperature min = {}\n
                    temperature max = {}\n
                    humidity min = {}\n
                    humidity max = {}\n
                    \n
                Actual value is:\n
                    temperature = {}\n
                    humidity = {}\n
                    timestamp = {}\n
            """.format(
                config[0],
                config[1],
                config[2],
                config[3],
                data[0],
                data[1],
                data[2]
            )
        else:
            self.__body = """
                Current value is:\n
                    temperature = {}\n
                    humidity = {}\n
                    timestamp = {}\n
                    status = {}\n
            """.format(
                data[0],
                data[1],
                data[2],
                data[3]
            )

    def get_message(self):
        """
        Getter for title and body
        """
        return self.__title, self.__body

    def send_notification(self):
        """ Sending notification via pushbullet.
            Args:
                title (str) : title of text.
                body (str) : Body of text.
        """
        data_send = {
            "type": "note",
            "title": self.__title,
            "body": self.__body
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
        print("complete sending")


def main():
    """
    Main Method
    """
    # Initialization
    data = Data()
    database = Database()
    notification = Notification()

    # Read temp and humid from sense hat sensor and Insert data into database
    database.insert_data(*data.read_data())

    # Get today data from the database
    today_data = database.read_data(today=True)

    # Get the worst data from the database and sort it
    bad_data = []
    for temp, humid, timestamp in today_data:
        # Calculate the difference
        diff = data.cal_out_of_range(temp, humid)
        # Create tuple of data with diff
        data_with_diff = (temp, humid, timestamp, diff)
        # Append to bad_data
        bad_data.append(data_with_diff)
    # Sort the bad_data by diff with highest diff as first element
    bad_data = sorted(bad_data, key=lambda x: x[-1], reverse=True)

    # Set notification limit
    limit = MAX_NOTIFICATION_PER_DAY * MAX_BAD_ITEM
    # Check if the notification limit is not reached
    if database.read_notification(limit):
        # Send MAX_BAD_ITEM notification from the worst data
        for bad in bad_data[:MAX_BAD_ITEM]:
            # Construct the notification message
            notification.set_message(bad[:-1], *data.read_config())
            # Send notification
            notification.send_notification()
            # Get notification message
            title, body = notification.get_message()
            # Insert a record of notification sent
            database.insert_notification(title, body, datetime.datetime.now())

    # Clear all object
    del data
    del database
    del notification


if __name__ == "__main__":
    main()
