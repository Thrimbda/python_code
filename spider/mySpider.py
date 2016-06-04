# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-05-22 15:35:19
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-05-22 16:23:01
import requests
from bs4 import BeautifulSoup

url = 'https://cas.xjtu.edu.cn/login?service=http%3A%2F%2Fssfw.xjtu.edu.cn%2Findex.portal'
postAction = 'https://cas.xjtu.edu.cn/login;jsessionid=09E4682337E55FFD00314378B433363C?service=http%3A%2F%2Fssfw.xjtu.edu.cn%2Findex.portal'


class MySpider:
    def __init__(self, url):
        self.url = url
