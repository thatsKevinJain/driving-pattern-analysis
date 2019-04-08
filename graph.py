import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('results-obd2.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append((row[0]))
        y.append((row[5]))

plt.plot(x,y, label='Total events occured')
plt.xlabel('Trip No.')
plt.ylabel('Number of events')
plt.title('Excessive Engine Load')
plt.legend()
plt.show()