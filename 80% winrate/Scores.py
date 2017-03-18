import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
fname = str(sys.argv[1])
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open(fname,"r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(x)
            yar.append(y)
    ax1.clear()
    ax1.plot(xar,yar)
    plt.xlabel("Total Amount Of Games")
    plt.ylabel("AI Scores")
    plt.title("Graph 1")
    plt.grid()
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
