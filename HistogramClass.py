# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-03-25 00:03:29
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-04-21 21:58:12
import numpy as np
import matplotlib.pyplot as plt

fileName = "/home/michael/Documents/Data/javaFibonacci.txt"

data = []
data.append(np.loadtxt(fileName, delimiter="\n"))
ticks = np.arange(len(data[0]))


def Histogram(data, yLabel, xLabel, ticks, title, plotNum=1):
    axs = []
    rects = []
    fig = plt.figure()
    for i in np.arange(plotNum):
        axs.append(fig.add_subplot(plotNum * 100 + 10 + i + 1))

    axs[0].set_title(title)

    for i in np.arange(plotNum):
        rects.append(axs[i].bar(ticks, data[i],
                     facecolor=(np.random.random(),
                                np.random.random(),
                                np.random.random()),
                     edgecolor='white'))
        axs[i].set_ylabel('time(ms)')
        axs[i].set_xlabel('magnitude(10^x)')
        axs[i].set_xticks(ticks)

        for x, y in zip(ticks, data[0]):
            axs[i].text(x + 0.4, 1.001 * y, '%d' % y, ha='center', va='bottom')

        axs[i].set_ylim(0, 1.1 * np.max(data[i]))
    return fig
    # plt.draw()

if __name__ == '__main__':
    fig = Histogram(data, 'time(ms)', 'magnitude(10^x)',
                    ticks, 'Select num index from disordered array')
    plt.show()
