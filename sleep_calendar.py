from os import close
import calendar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import csv

def convert_time(time):
    time = time.split(' ')
    hm = time[0].split(':')
    h = int(hm[0])
    m = int(hm[1])
    if time[1] == "pm" and h < 12:
        h += 12 
    if time[1] == "am" and h == 12:
        h -= 12

    return h + (m/60)


#Gets the data from csv-file
def get_data():
    with open('fitbit_export_20210516.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        data = list(csv_reader)

        #The month currently being used (only works if all data is from the same month)
        month = data[3][0][3:5]

        day, start, end = [], [], []

        #List of sleep including date,start,end
        for row in data[2:]: 
            if not row:
                continue
            day.append(int(row[0][:2]))
            start.append(convert_time(row[0][11:]))
            end.append(convert_time(row[1][11:]))

    file.close()
    return day, start, end


#Plots the calendar using data from method above
def create_calendar(day, start, end):
    plt.figure(figsize=(12,7))
    ax = plt.gca().axes

    #adds labels
    plt.yticks(np.arange(1, 32))
    plt.xticks(np.arange(1,25))
    plt.ylim(32, 1)
    plt.xlim(1,25)

    data = pd.DataFrame({"start": start, "end": end})

    for s, e in zip(data['start'].values, data['end'].values):
        ax.add_patch(Rectangle((s, day.pop(0)), width=(e-s), height=.3, color='cyan'))


    #removes ticks and borders
    plt.tick_params(left=False, bottom=False)
    [spine.set_visible(False) for spine in plt.gca().spines.values()]

    #show figure
    plt.show()

day, start, end = get_data()
create_calendar(day, start, end)