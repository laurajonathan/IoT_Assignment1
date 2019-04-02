"""
analytics.py

Created by Suwat Tangtragoonviwatt (s3710374) and Laura Jonathan (s3696013)

This script is show data visualization

"""

import matplotlib.pyplot as plt
import csv

with open('report.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')



sizes = [70, 30]
labels = ["OK", "BAD"]

plt.pie(sizes, labels = labels, autopct = "%.2f")
plt.axes().set_aspect("equal")
plt.title("Proportion of OK status and bad status")
plt.show()