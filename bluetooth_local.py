"""
bluetooth.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to send the current value of temperature and
humidity from sense hat sensor via Pushbullet when a device is connected.

"""

import time
import subprocess as sp
import bluetooth as bt
from monitor_and_notify import Data
from monitor_and_notify import Notification
from create_report import Report

DELAY = 5


class Bluetooth:
    """
    Bluetooth class to detect the nearby bluetooth device and
    send the message via Pushbullet when a device is connected
    """
    def __init__(self):
        self.__nearby_devices = []
        self.__paired_devices = []

    def scan_nearby_device(self):
        """
        Scan nearby device mac address
        """
        print("Scanning...")
        nearby_devices = bt.discover_devices()
        devices = []
        for mac_address in nearby_devices:
            devices.append(mac_address)
        self.__nearby_devices = devices

    def list_paired_device(self):
        """
        List paired device with bt-device --list command and
        store mac address of all devices list
        """
        # Run bt-device --list command
        paired_devices = sp.Popen(
            ["bt-device", "--list"],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            close_fds=True
        )
        # Read output from stdout
        device_list_from_stdout = paired_devices.stdout
        device_list = device_list_from_stdout.readlines()

        # Decode output from binary to string
        devices = []
        for device in device_list:
            devices.append(device.decode("utf-8"))

        # Get the devices list without the header
        device_list = devices[1:]

        # Extract devices mac address
        devices = []
        for device in device_list:
            devices.append(device[-19:-2])

        self.__paired_devices = devices

    def get_nearby_paired_devices(self):
        """
        Get the nearby device that paired with raspberry pi before
        """
        devices = []
        for device in self.__nearby_devices:
            if device in self.__paired_devices:
                devices.append(device)
        return devices


def main():
    """
    Main Method
    """
    # Initialization
    bluetooth = Bluetooth()
    data = Data()
    notification = Notification()
    report = Report(data)

    while True:
        # Scan nearby device
        bluetooth.scan_nearby_device()
        # List nearby device
        bluetooth.list_paired_device()

        # Get nearby paired device
        for device in bluetooth.get_nearby_paired_devices():
            # Set notification title
            title = "Device %s is nearby send real time data" % device
            # Get current data
            current_data = data.read_data()
            # Generate status with (temp, humid)
            status = report.generate_status(current_data[0], current_data[1])
            # Set message
            message = current_data + (status,)
            # Set notification message with current data
            notification.set_message(message, title=title)
            # Send notification
            notification.send_notification()

        # Delay before the next scan
        time.sleep(DELAY)

    # Clear all object
    del bluetooth
    del data
    del notification


if __name__ == "__main__":
    main()
