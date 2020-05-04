'''
@author: kalarita
@Date: 2020-05-04 08:16:11
@LastEditors: kalarita
@LastEditTime: 2020-05-04 12:38:28
'''
import json
import sqlite3
import uuid

from flask import Flask, make_response, request
import hashlib

app = Flask(__name__)

#创建数据库,返回一个打开的数据库连接
def createDb():
    conn = sqlite3.connect('usr.db')
    cursor = conn.cursor()
    sql = '''CREATE TABLE usr (
        name varchar,
        id varchar,
        mail varchar,
        pwd varchar,
        primary key(id)
    )
                '''
    cursor.execute(sql)
    conn.commit()
    return conn

#返回一个打开的数据库连接
def  connectDb(dbName):
    try:
        conn = sqlite3.connect(dbName)
    except:
        print("could not connect to database!")
        conn = createDb()
    return  conn

#注册接口,返回success为注册成功,fail为注册失败
@app.route('/register/<Secretkey>',methods = ['get'])
def register(Secretkey):                #通过传入的账户名,邮箱和密码,生成id,同时对密码进行加盐加密
    conn = connectDb('C:\\canlendarProject\\DiaryCanlendar\\usr.db')
    cursor = conn.cursor()
    sqlall = 'select *from usr'
    beforetotal = len(cursor.execute(sqlall).fetchall())
    lst = Secretkey.split('+')
    print(lst)
    id = generateId(lst)
    print('id='+id+str(type(id)))
    shapwd = hashlib.sha1((lst[2]+lst[1][2:6]).encode('utf-8')).hexdigest()
    name = lst[0]
    mail = lst[1]
    sql = 'insert into usr values (?,?,?,?)'
    try:
        cursor.execute(sql,(name,id,mail,shapwd))
    except:
        result = 'fail'
    aftertotal = len(cursor.execute(sqlall).fetchall())
    if aftertotal-beforetotal ==1:
        result = "success"
    else:
        result = "fail"
    # print(conn.execute(sqlall).fetchall())
    conn.commit()
    conn.close()
    return result
#使用uuid根据用户的邮箱产生不同的id
def generateId(lst):
    id = uuid.uuid3(uuid.NAMESPACE_DNS,lst[1])
    id = str(id)
    return id

