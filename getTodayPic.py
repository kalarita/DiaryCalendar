'''
@author: kalarita
@Date: 2020-05-03 21:45:03
@LastEditors: kalarita
@LastEditTime: 2020-05-03 22:41:05
'''
import requests
import logging

def getPic(url):
    try:
        r = requests.get(url)
        
    except:
        print("cannot connect to target website")
        logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='pic.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    #日志格式
                    )
        logger = logging.getLogger(__name__)
        logger.debug("could not get the picture")
    return r
def main():
    url = "https://source.unsplash.com/random/800x600"
    response = getPic(url)
    with open("today.jpg","wb") as f:
        f.write(response.content)

if __name__ == "__main__":
    main()