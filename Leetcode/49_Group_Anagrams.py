# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-03-12 14:04:14
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-05-15 10:18:25


class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        hashTable = {}
        for i in strs:
            listI = list(i)
            listI.sort()
            listI = tuple(listI)
            if hashTable.get(listI) is not None:
                res = hashTable.get(listI)
                res.append(i)
                res.sort()
                hashTable[listI] = res
            else:
                hashTable[listI] = [i]
        res = list(hashTable.values())
        res.sort()
        return(res)

if __name__ == '__main__':
    a = ['tea', 'ate', 'aet', 'break', 'baerk']
    b = Solution()
    print(b.groupAnagrams(a))
