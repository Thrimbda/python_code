# -*- coding: utf-8 -*-
# @Author: michael
# @Date:   2016-04-30 17:23:29
# @Last Modified by:   michael
# @Last Modified time: 2016-05-02 01:39:11
import csv


class DataFilter:
    def __init__(self, wfileName, *rfileName):
        try:
            self.rfileobj = []
            for item in rfileName:
                self.rfileobj.append(open(item, 'r'))
            self.wfileobj = open(wfileName, 'w')
            self.data = []
            for item in range(len(self.rfileobj)):
                self.data.append([])
            # self.data = self.rfileobj.readlines()[startLine:endLine]
        except IOError:
            print("faile to open file. please check your file name.")
            for item in self.rfileobj:
                item.close()
            self.wfileobj.close()

    def csvExtract(self, col1, col2):
        self.csvDataRead()
        schoolName = []
        for item in self.data[1]:
            schoolName.append(item[col1])

        self.schoolList = []
        for school in self.data[0]:
            if school[col2] in schoolName:
                self.schoolList.append(school)
        writer = csv.writer(self.wfileobj)
        for item in self.schoolList:
            writer.writerow(item)
        for item in self.rfileobj:
            item.close()
        self.wfileobj.close()

    def dataClean(self):
        self.csvDataRead()
        writer = csv.writer(self.wfileobj)
        varList = []
        for i in range(len(self.data[0][0])):
            # print(i)
            for item in self.data[0]:
                varList.append(item[i])
            writer.writerow(varList)
            # print(varList)
            varList = []
        self.wfileobj.close()

    def csvDataRead(self):
        reader = []
        for item in self.rfileobj:
            reader.append(csv.reader(item))
            # print(reader[0])
        for item in range(len(reader)):
            for obj in reader[item]:
                self.data[item].append(obj)

    def dataFilt(self, *col):
        self.csvDataRead()
        self.filtedData = []
        for item in self.data[0]:
            line = []
            for i in range(len(col)):
                line.append(item[col[i]])
            self.filtedData.append(line)

if __name__ == '__main__':
    myFilter = DataFilter('/home/michael/Documents/MCM/2016校内赛题目/C题/ProblemCDATA/cleanDataInput.csv', '/home/michael/Downloads/data.csv')
    myFilter.dataClean()
