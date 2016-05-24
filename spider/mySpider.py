# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-05-22 15:35:19
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-05-24 19:59:41
import requests
from bs4 import BeautifulSoup
# from collections import deque

url = 'https://cas.xjtu.edu.cn/login?service=http%3A%2F%2Fssfw.xjtu.edu.cn%2Findex.portal'
headers = {'Connection': 'keep-alive',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Referer': 'https://www.baidu.com/link?url=YEhWaYGOPw1mlBWWji4kqYkbuQYoRfmYE94YXDz7Dwm&wd=&eqid=d69a671b000e59e70000000357406ffe',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36',
           }

with requests.Session() as sission:
    bean = BeautifulSoup(sission.get(url).text, 'html.parser')
    # csrfmiddlewaretoken = bean.find("input", {'name': 'csrfmiddlewaretoken'})['value']
    lt = bean.find("input", {'name': 'lt'})['value']
    execution = bean.find("input", {'name': 'execution'})['value']
    _eventId = bean.find("input", {'name': '_eventId'})['value']

    myForm = {'username': 'siyuan.mac', 'password': '960627Oo', 'lt': lt, 'execution': execution, '_eventId': _eventId}
    cookies = sission.post(url, myForm, headers=headers)
    print(cookies)
    response = sission.get('http://ssfw.xjtu.edu.cn/index.portal', cookies=cookies.cookies)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.body.text)

    for i in soup.find_all("a"):
        subUrl = i.get('href')
        if 'http' not in subUrl and subUrl != '#':
            subUrl = 'http://ssfw.xjtu.edu.cn/index.portal' + subUrl
        print(subUrl)
    # print(soup.body.tr)
