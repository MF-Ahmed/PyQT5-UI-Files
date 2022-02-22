import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

cnt=0

x_vals = []
y_vals = []

index = count()

def animate(i):
    x_vals.append(next(index))
    print(x_vals)
    y_vals.append(random.randint(0, 90))
    print(y_vals)

    if (i > 10):  # If you have 50 or more points, delete the first one from the array
        y_vals.pop(0)  # This allows us to just see the last 50 data points
        x_vals.pop(0)

    plt.cla()
    plt.ylim(0,100)
    plt.plot(x_vals,y_vals,'ro-')




#ani = FuncAnimation(plt.gcf(), animate, interval=100)

#plt.tight_layout()
#plt.show()


# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']