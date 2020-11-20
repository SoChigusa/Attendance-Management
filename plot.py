import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print('Now plotting...')

# cf. transformation from date string to serial #
# tstr = datetime.strptime('2020/11/14', '%Y/%m/%d') - datetime(1970,1,1)
# print(tstr.days)

# figure settings and data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Workloads and Moods : So Chigusa', size=20)
data = np.loadtxt('atm.dat', usecols=range(3), delimiter='\t', skiprows=1)

# line plot
ax.plot(data[:,0], data[:,1], zorder=1)

# scatter plot
color = ['red', 'orange', 'blue']
def plotFeeling(array):
    ax.scatter(array[0], array[1], color=color[int(array[2])], zorder=2)
np.apply_along_axis(plotFeeling, 1, data)

# x-axis
def serial2date(num):
    return (datetime(1970,1,1) + timedelta(days=num)).strftime('%Y/%m/%d')
dt = np.vectorize(serial2date)(data[:,0])
center1 = (int)(np.floor(dt.size/3))
center2 = (int)(np.floor(2*dt.size/3))
ax.set_xlabel('Date', size=15)
ax.set(xticks=[data[0,0],data[center1,0],data[center2,0],data[-1,0]],\
       xticklabels=[dt[0],dt[center1],dt[center2],dt[-1]])

# y-axis
ax.set_ylim(-0.1, 3.1)
ax.set_ylabel('How hard did you work?', size=15)
ax.set(yticks=[0,1,2,3], yticklabels=['hardly', 'a little', 'well', 'hard'])

# legend
ax.scatter(data[0,0], 100, color=color[2], label='cheerful')
ax.scatter(data[0,0], 100, color=color[1], label='soso')
ax.scatter(data[0,0], 100, color=color[0], label='depressed')
ax.legend(fontsize=15, loc='best')

plt.tight_layout()
plt.savefig('plot.png', bbox_inches='tight')
