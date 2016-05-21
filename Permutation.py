# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-04-06 21:42:26
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-05-19 11:34:06


def permutationR(mylist, low, high):
    if low == high:
        print(mylist)
    else:
        for i in range(low, high + 1):
            mylist[low], mylist[i] = mylist[i], mylist[low]
            permutationR(mylist, low + 1, high)
            mylist[low], mylist[i] = mylist[i], mylist[low]


def permutationS(mylist, low, high):
    pass


if __name__ == '__main__':
    mylist = ['a', 'b', 'c', 'd', 'e']
    permutationR(mylist, 0, 4)
