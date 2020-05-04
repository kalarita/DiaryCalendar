'''
@author: kalarita
@Date: 2020-05-04 10:52:19
@LastEditors: kalarita
@LastEditTime: 2020-05-04 19:25:56
'''
import requests
import json

r = requests.get('http://127.0.0.1:5000/todayidea')
# print(type(json.loads(r.text)))
print(r.content)
print(r.text)
print(r)