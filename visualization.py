import matplotlib.pyplot as plt
from random import randint
from matplotlib.animation import FuncAnimation


plt.style.use("fivethirtyeight")

# open figure
fig = plt.figure()
# add grid specifications
gs = fig.add_gridspec(2, 3)
# open axes/subplots
axes = []
axes.append(fig.add_subplot(gs[:, 0:2]))  # large subplot (2 rows, 2 columns)
axes.append(fig.add_subplot(gs[0, 2]))   # small subplot (1st row, 3rd column)
axes.append(fig.add_subplot(gs[1, 2]))   # small subplot (2nd row, 3rd column)

x_vals = []
y_vals = []

def animate(i):
    x_vals.append(randint(0, 100))
    y_vals.append(randint(1, 5))
    axes[0].clear()
    axes[0].plot(x_vals, y_vals)
    axes[0].bar(x_vals, y_vals)


animation_obj = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.show()