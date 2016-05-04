# -*- coding: utf-8 -*-
# @Author: michael
# @Date:   2016-05-01 21:49:32
# @Last Modified by:   michael
# @Last Modified time: 2016-05-02 10:32:47

import numpy as np
import matplotlib.pyplot as plt
import dataFilter


class K_means:
    def __init__(self, dataSet, k=5):
        self.k = k
        self.dataSet = dataSet

    def initCentroids(self):
        numSamples, dim = self.dataSet.shape
        self.centroids = np.zeros((self.k, dim))
        for i in np.arange(self.k):
            index = int(np.random.uniform(0, numSamples))
            self.centroids[i, :] = self.dataSet[index, :]

    def kmeans(self):
        numSamples = self.dataSet.shape[0]

        self.clusterAssment = np.mat(np.zeros((numSamples, 2)))
        clusterFlag = True

        self.initCentroids()

        while clusterFlag:
            clusterFlag = False

            for i in np.arange(numSamples):
                minDist = 100000.0
                minIndex = 0

                for j in np.arange(self.k):
                    distance = np.sqrt(np.sum(np.power(self.centroids[j, :] - self.dataSet[i, :], 2)))
                    if distance < minDist:
                        minDist = distance
                        minIndex = j

                if self.clusterAssment[i, 0] != minIndex:
                    clusterFlag = True
                    self.clusterAssment[i, :] = minIndex, minDist ** 2

            for j in np.arange(self.k):
                pointsInCluster = self.dataSet[np.nonzero(self.clusterAssment[:, 0].A == j)[0]]
                self.centroids[j, :] = np.mean(pointsInCluster, axis=0)

        print('clusting complete.')


def showCluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Your k is too large! please contact Zouxy")
        return 1

    # draw all samples
    for i in np.arange(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    # draw the centroids
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i], markersize=12)

    plt.show()


if __name__ == '__main__':
    myDataFilter = dataFilter.DataFilter('/home/michael/Documents/MCM/2016校内赛题目/C题/ProblemCDATA/dataSet.csv', '/home/michael/Downloads/data.csv')
    myDataFilter.dataFilt(137, 140)
    dataSet = []
    for item in myDataFilter.filtedData[1:]:
        line = []
        for i in range(len(item)):
            line.append(float(item[i]))
        dataSet.append(line)
    dataSet = np.mat(dataSet)
    k = 3
    kmeans = K_means(dataSet, k)
    kmeans.kmeans()
    print(kmeans.centroids)
    showCluster(dataSet, k, kmeans.centroids, kmeans.clusterAssment)
