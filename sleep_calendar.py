from os import close
import itertools
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numpy.core.defchararray import center
import pandas as pd
import csv
import datetime
from datetime import datetime as dt

def convert_time(time):
    seconds = (time.hour * 60 + time.minute) * 60 + time.second
    return seconds/3600



DATE_FORMAT = "%d-%m-%Y %I:%M %p"

sleep_intervals = []

def get_data():
    with open('fitbit_export_20210516.csv') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(itertools.islice(csv_reader, 2, 2), None)

        #Iterates through rows in file
        for row in csv_reader:
            if not row or len(row) < 2:
                continue

            #Adds sleep intervals as custom datetimes
            sleep_intervals.append((dt.strptime(row[0], DATE_FORMAT), dt.strptime(row[1], DATE_FORMAT)))
    
    file.close()

    start_date = min([sleep[0] for sleep in sleep_intervals])
    end_date = max([sleep[1] for sleep in sleep_intervals])
    num_days = (end_date - start_date).days + 1

    #start_date = start_time.date()
    #end_date = end_time.date()

    return(sleep_intervals, start_date, end_date, num_days)


#Plots the calendar using data from method above
def create_calendar(sleep, start, end, day):

    fig, ax = plt.subplots()

    ax.set_yticks(range(days))
    ax.set_yticklabels([(end - datetime.timedelta(days=i)).date() for i in range(days)], fontdict={'verticalalignment':'bottom'})

    ax.set_xticks(range(24))
    ax.set_xticklabels([(dt.combine(datetime.date(1,1,1), datetime.time(20, 0, 0)) + datetime.timedelta(hours=j)).time() for j in range(24)])
    fig.autofmt_xdate()

    iter_day = end.day
    for begin, stop in sleep:
        s = convert_time(begin)
        e = convert_time(stop)
        day = iter_day - begin.day

        #if begin.day != stop.day:
        #    continue

        ax.add_patch(Rectangle((s + 4, day), e-s, .8, color='cyan'))

    plt.show()


"""
    data = pd.DataFrame({"start": start, "end": end})

    for s, e in zip(data['start'].values, data['end'].values):
        ax.add_patch(Rectangle((s, day.pop(0)), width=(e-s), height=.4, color='cyan'))


    #removes ticks and borders
    plt.tick_params(left=False, bottom=False)
    [spine.set_visible(False) for spine in plt.gca().spines.values()]

    #show figure
    fig.align_labels()
    plt.show()

"""

sleep, start, end, days = get_data()
create_calendar(sleep, start, end, days)