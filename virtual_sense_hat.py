"""
virtual_sense_hat.py

Created by: Matthew Bolger

Modified by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to simulate the sense hat sensor
in case of the sense hat is not working or not connected.

If sense hat is working correctly this module will return sense hat

"""

import logging
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
    def getSenseHat(logError=True):
        try:
            return SenseHat()
        except Exception as e:
            if(logError):
                logging.error("Use VirtualSenseHat because: " + str(e))
            return VirtualSenseHat()

    def get_temperature(self, min_value=1000, max_value=3000):
        return random.randint(min_value, max_value) / 100

    def get_humidity(self, min_value=5000, max_value=6000):
        return random.randint(min_value, max_value) / 100

    def show_message(self,
                     text_string,
                     scroll_speed=0.1,
                     text_colour=[255, 255, 255],
                     back_colour=[0, 0, 0]
                     ):
        print(text_string)

    def clear(self):
        pass
