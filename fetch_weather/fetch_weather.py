#!/usr/bin/env python

import urllib2
import json
import string

def get_int(str):
    i = 0
    while i < len(str):
        if str[i] < '0' or str[i] > '9':
            break
        i = i + 1
    return str[0:i]
fetch_url = 'http://www.weather.com.cn/data/cityinfo/'
city_ids = ['101010100', '101020100', '101030100', '101040100']
for i in city_ids:
    content = urllib2.urlopen(fetch_url + i + '.html').read()
    weather = json.loads(content)
    if len(weather) >= 1:
        print weather['weatherinfo']['cityid'] , weather['weatherinfo']['city'], get_int(weather['weatherinfo']['temp1']), get_int(weather['weatherinfo']['temp2'])
