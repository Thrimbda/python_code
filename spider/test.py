# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-04-19 17:12:04
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-05-21 19:49:26
import urllib.request
import urllib
# import os
import re
from collections import deque


queue = deque()
visited = set()

url = 'https://www.douban.com/'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()
    visited |= {url}

    print('already grabed:' + str(cnt) + '    grabing <---  ' + url)
    cnt += 1
    urlop = urllib.request.urlopen(url, timeout=2)
    if 'html' not in urlop.getheader('Content-Type'):
        continue

    try:
        data = urlop.read().decode('utf-8')
    except Exception as e:
        print(e)
        continue

    linkre = re.compile('href="(.+?)"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('appended queue --->' + x)
