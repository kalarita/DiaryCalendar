'''
@author: kalarita
@Date: 2020-05-04 10:52:19
@LastEditors: kalarita
@LastEditTime: 2020-05-04 11:27:56
'''
import requests

r = requests.get('http://127.0.0.1:5000/register/fuckyou+1078950499@qq.com+bcs@12345')
print(r.text)
print(r)