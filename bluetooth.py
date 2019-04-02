"""
bluetooth.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is intended to update the temperature and humidity every minutes.

"""

import bluetooth as bt
import time
import subprocess as sp
from monitorAndNotify import Data
from monitorAndNotify import Notification

DELAY = 1


class Bluetooth:
    """
    Bluetooth class to detect the nearby bluetooth device and
    send the message via Pushbullet when a device is connected
    """
    def __init__(self):
        pass

    def scan_nearby_device(self):
        """
        Scan nearby device mac address
        """
        nearby_devices = bt.discover_devices()
        devices = []
        for mac_address in nearby_devices:
            devices.append(mac_address)
        return devices

    def list_paired_device(self):
        """
        List paired device with bt-device --list command and
        return mac address of all devices list
        """
        paired_devices = sp.Popen(
            ["bt-device", "--list"],
            stdin=sp.PIPE,
            stdout=sp.PIPE,
            close_fds=True
        )
        device_list_from_stdout = paired_devices.stdout
        device_list = device_list_from_stdout.readlines()

        devices = []
        for device in device_list:
            devices.append(device.decode("utf-8"))

        # Get the devices list without the header
        device_list = devices[1:]

        # Extract devices mac address
        devices = []
        for device in device_list:
            devices.append(device[-19:-2])

        return devices


def main():
    """
    Main Method
    """
    # Initialization
    bluetooth = Bluetooth()
    data = Data()
    notification = Notification()

    while True:
        nearby_device = bluetooth.scan_nearby_device()
        paired_device_list = bluetooth.list_paired_device()
        print("Device: %s" % paired_device_list)
        temp, humid, timestamp = data.read_data()
        print(temp, humid, timestamp)
        time.sleep(DELAY)
    
        
    
    print(bluetooth.list_paired_device())


if __name__ == "__main__":
    main()
