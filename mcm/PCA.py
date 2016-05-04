# -*- coding: utf-8 -*-
# @Author: michael
# @Date:   2016-05-01 17:44:48
# @Last Modified by:   michael
# @Last Modified time: 2016-05-01 17:46:22
import numpy as np


def pca(dataMat, topNfeat=9999999):
    meanVals = np.mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals
    # remove mean
    covMat = np.cov(meanRemoved, rowvar=0)
    eigVals, eigVects = np.linalg.eig(np.mat(covMat))
    eigValInd = np.argsort(eigVals)
    # sort, sort goes smallest to largest
    eigValInd = eigValInd[:-(topNfeat + 1):-1]
    # cut off unwanted dimensions
    redEigVects = eigVects[:, eigValInd]
    # reorganize eig vects largest to smallest
    lowDDataMat = meanRemoved * redEigVects
    # transform data into new dimensions
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat
