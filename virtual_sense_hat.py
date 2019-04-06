"""
virtual_sense_hat.py

Created by: Matthew Bolger

Modified by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to simulate the sense hat sensor
in case of the sense hat is not working or not connected.

If sense hat is working correctly this module will return sense hat

"""

import random

try:
    from sense_hat import SenseHat
except ImportError:
    pass


class VirtualSenseHat:
    """
    Defined VirtualSenseHat class to simulate the sense hat
    """

    @staticmethod
    def get_sense_hat():
        """
        If SenseHat module exist use SenseHat
        else use VirtualSenseHat
        """
        try:
            return SenseHat()
        except NameError:
            return VirtualSenseHat()

    @classmethod
    def get_temperature(cls, min_value=1000, max_value=3000):
        """
        Return random temperature in range (10, 30)
        """
        return random.randint(min_value, max_value) / 100

    @classmethod
    def get_humidity(cls, min_value=5000, max_value=6000):
        """
        Return random humidity in range (50, 60)
        """
        return random.randint(min_value, max_value) / 100

    @classmethod
    def show_message(cls, text_string):
        """
        Print message on the console
        """
        print(text_string)

    def clear(self):
        """
        Mimic SenseHat clear
        """
        pass
