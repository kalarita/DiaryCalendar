'''
@author: kalarita
@Date: 2020-05-03 22:07:03
@LastEditors: kalarita
@LastEditTime: 2020-05-03 22:59:24
'''
import json
import logging

import requests


def getIdea(url):
    try:
        r = requests.get(url)
        response = r
    except:
        logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='idea.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
        logger = logging.getLogger(__name__)
        logger.debug("could not get the idea")
    return response

def main():
    url = "https://apiv3.shanbay.com/weapps/dailyquote/quote/"
    response = getIdea(url)
    response = json.loads(response.text)
    with open("Idea.txt","w+") as f:
        f.write(response['content']+"\n")
        f.write(response['translation']+'--'+response['author'])

if __name__ == "__main__":
    main()
