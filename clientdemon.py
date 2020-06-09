'''
@author: kalarita
@Date: 2020-05-04 10:52:19
@LastEditors: kalarita
@LastEditTime: 2020-05-06 09:08:30
'''
import requests
import json

# r = requests.get('http://173.82.168.215:5000/register/kalarita+bcs4real@outlool.com+bcs@12345')
r = requests.get('http://127.0.0.1:5000/login/bcs4real@outlool.com+bcs@12345')
# print(type(json.loads(r.text)))
# print(r.content)
print(r.text)
print(r)
# for i in json.loads(r.content):
#     print(i)