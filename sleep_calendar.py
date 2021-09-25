from os import close
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from numpy.core.defchararray import center
import csv
import datetime
from datetime import datetime as dt

def convert_time(time):
    seconds = (time.hour * 60 + time.minute) * 60 + time.second
    return seconds/3600

DATE_FORMAT = "%d-%m-%Y %I:%M %p"

sleep_intervals = []

def get_data():
    with open('') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(itertools.islice(csv_reader, 2, 2), None)

        #Iterates through rows in file
        for row in csv_reader:
            if not row or len(row) < 2:
                continue

            #Adds sleep intervals as custom datetimes
            sleep_intervals.append((dt.strptime(row[0], DATE_FORMAT), dt.strptime(row[1], DATE_FORMAT)))
    
    file.close()

    #Start and end days for period, number of days
    start_date = min([sleep[0] for sleep in sleep_intervals])
    end_date = max([sleep[1] for sleep in sleep_intervals])
    num_days = (end_date - start_date).days + 1

    return(sleep_intervals, start_date, end_date, num_days)


#Plots the calendar using data from method above
def create_calendar(sleep, start, end, days):

    fig, ax = plt.subplots()

    #Sets labels based on datetiems. Iterates backwards
    ax.set_yticks(range(days + 1)) 
    ax.set_yticklabels([(end - datetime.timedelta(days=i)).date() for i in range(days + 1)], fontdict={'verticalalignment':'bottom'})

    #Sets labels based on times
    ax.set_xticks(range(24))
    ax.set_xticklabels([(dt.combine(datetime.date(1,1,1), datetime.time(20, 0, 0)) + datetime.timedelta(hours=j)).time() for j in range(24)])

    #Adjusts overlapping labels
    fig.autofmt_xdate()

    #Calculates the intervals
    avg_start = 0
    iter_day = end.day
    for begin, stop in sleep:
        s = convert_time(begin)
        e = convert_time(stop)
        day = iter_day - begin.day
        
        #Moves the interval one day later when time crosses midnight
        if begin.day != stop.day:
            day = iter_day - stop.day
        
        #The graph ends and starts at 20 o'clock, this moves it left. 
        if s > 20: 
            s -= 24

        #For when the interval crosses 20 o'clock
        if s < 20 < e: 
            ax.add_patch(Rectangle((s + 4, day), 20, .8, color='gray'))
            s = - 4
            e -= 24
            day = day - 1

        #Draws sleep intervals
        ax.add_patch(Rectangle((s + 4, day), e-s, .8, color='gray'))

        avg_start += s
    
    avg_start = (avg_start / len(sleep_intervals)) + 4
    plt.axvline(x=avg_start, label='Avg. falling asleep time', c='red')
    plt.legend()
    plt.grid(axis = 'x', linestyle = '--')
    plt.show()


#Processes data
sleep, start, end, days = get_data()

#Creates and shows calendar
create_calendar(sleep, start, end, days)