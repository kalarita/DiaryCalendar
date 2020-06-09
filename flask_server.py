'''
@author: kalarita
@Date: 2020-05-04 08:16:11
@LastEditors: kalarita
@LastEditTime: 2020-05-06 09:23:45
@note:部署完成之后我才想起来服务器时间还得注意,现在只是暂时调了一下,不清楚重启之后定时任务的情况
'''
import json
import sqlite3
import uuid
import os

from flask import Flask, make_response, request,Response
import hashlib
from flask.json import jsonify

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


#接下来三个函数是在flask运行的时候直接把当天需要获取的数据类型直接放到内存中,并且常驻,在每次需要用的时候可以直接获取,减少硬盘IO
def get_his():
    hisresult = []
    with open('today.txt','r')as f:
        lines = f.readlines()
        for line in lines:
            hisresult.append(line)
    return hisresult

def get_img():
    with open('today.jpg','rb')as f:
        image = f.read()
    return image

def get_idea():
    idearesult = []
    with open('Idea.txt','r')as f:
        lines = f.readlines()
        for line in lines:
            idearesult.append(line)
    return idearesult

#初始化三个常驻变量
todayinhis = get_his()
image = get_img()
idea = get_idea()

#创建数据库,返回一个打开的数据库连接
def createDb():
    conn = sqlite3.connect('usr.db')
    cursor = conn.cursor()
    sql = '''CREATE TABLE usr (
        name varchar,
        id varchar,
        mail varchar,
        pwd varchar,
        primary key(mail)
    )
                '''
    cursor.execute(sql)
    conn.commit()
    return conn

#返回一个打开的数据库连接
def  connectDb(dbName):
    if os.path.exists('usr.db'):
        conn = sqlite3.connect(dbName)   
    else:
        print("could not connect to database!")
        conn = createDb()
    return  conn

#注册接口,返回success为注册成功,fail为注册失败
@app.route('/register/<Secretkey>',methods = ['get'])
def register(Secretkey):                #通过传入的账户名,邮箱和密码,生成id,同时对密码进行加盐加密
    conn = connectDb('usr.db')
    cursor = conn.cursor()
    sqlall = 'select *from usr'
    beforetotal = len(cursor.execute(sqlall).fetchall())
    lst = Secretkey.split('+')
    print(lst)
    id = generateId(lst)
    print('id='+id+str(type(id)))
    shapwd = hashlib.sha1((lst[2]+lst[1][2:6]).encode('utf-8')).hexdigest() #盐值为账户的2-6位
    name = lst[0]
    mail = lst[1]
    sql = 'insert into usr values (?,?,?,?)'
    try:
        cursor.execute(sql,(name,id,mail,shapwd))
    except:
         resp=make_response(jsonify(ststus='alreadyregisted',account=mail))
    aftertotal = len(cursor.execute(sqlall).fetchall())
    if aftertotal-beforetotal ==1:
        resp=make_response(jsonify(ststus='registed',account=mail))
    else:
        resp=make_response(jsonify(ststus='alreadyregisted',account=mail))
    # print(conn.execute(sqlall).fetchall())
    conn.commit()
    conn.close()
    return resp
#使用uuid根据用户的邮箱产生不同的id
def generateId(lst):
    id = uuid.uuid3(uuid.NAMESPACE_DNS,lst[1])
    id = str(id)
    return id

#登录接口
@app.route('/login/<account>')
def varify(account):
    result = 'fail'
    #假设传进来的account值为邮箱+密码,例如1078950499@qq.com+bcs@12345
    accountlst = account.split('+')
    print(accountlst)
    conn = connectDb('usr.db')
    cursor = conn.cursor()
    sql = 'select pwd from usr where mail=\''+str(accountlst[0])+'\''
    print(sql)
    print(cursor.execute(sql).fetchall())
    if len(cursor.execute(sql).fetchall()[0])>0:
        fetchedpwd = cursor.execute(sql).fetchall()[0][0]
    else:
        fetchedpwd = ''
    total = len(cursor.execute(sql).fetchall())
    if total>0:
        print(fetchedpwd)
        shapwd = hashlib.sha1((accountlst[1]+accountlst[0][2:6]).encode('utf-8')).hexdigest()
        print(shapwd)
        if fetchedpwd == shapwd:
            resp=make_response(jsonify(login='True',account = accountlst[0],msg = 'login success!'))
        else:
            resp=make_response(jsonify(login='False',account = accountlst[0],msg = 'please check your account or your password!'))
    else:
        resp=make_response(jsonify(login='False',account = accountlst[0],msg = 'please check your account or your password!'))
    return resp

#获取历史上的今天信息
@app.route('/todayinhis',methods=['get'])
def respond():
    resp = make_response(jsonify(todayinhis))
    return resp

#获取今日图片
@app.route('/todaypic',methods=['get'])
def respondpic():
    resp = Response(image,mimetype='image/jepg')
    return resp

#获取今日idea
@app.route('/todayidea',methods=['get'])
def respondidea():
    resp = make_response(jsonify(idea))
    return resp