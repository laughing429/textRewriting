#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# Create on: 2018-08-06
# Author: Lyu 
# Annotation:

import requests

req = requests.post('http://192.168.6.120:11111/1101/content_gen/', data={'data':'星期五到了，真开心啊！', 'count':3})
print(req.json())
