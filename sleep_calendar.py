from os import close
import calendar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import csv

#Gets the data from csv-file
def get_data():
    with open('fitbit_export_20210516.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        data = list(csv_reader)

        #The month currently being used (only works if all data is from the same month)
        month = data[3][0][3:5]

        #List of sleep including date,start,end
        sleep_data = []
        for row in data[2:]: 
            if not row:
                continue
            date = row[0][:2]
            start = row[0][11:]
            end = row[1][11:]
            sleep_data.append([date, start, end])

    file.close()
    return sleep_data
    


def create_calendar(sleep_data):
    #plt.figure(figsize=(10,10))
    #ax = plt.gca().axes
    #plt.show

sleep_data = get_data()
create_calendar(sleep_data)