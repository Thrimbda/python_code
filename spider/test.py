# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-04-19 17:12:04
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-04-21 00:03:42
import urllib.request
import urllib
import os


data = {}
data['word'] = 'node.js'

url_values = urllib.parse.urlencode(data)
url = 'http://www.baidu.com/s?'
full_url = url + url_values

data = urllib.request.urlopen(full_url).read()
data = data.decode('utf8')
print(data)
with open(os.path.split(os.path.realpath(__file__))[0]+'/myTest.txt', 'w') as fobj:
    fobj.write(data)
