
import pymongo
from requests import Session
from pyquery import PyQuery as pq
import time
import base64

client=pymongo.MongoClient(host='127.0.0.1',port=27017)

url='http://music.163.com/weapi/v1/resource/comments/R_SO_4_457207812?csrf_token=0db47dc21ce0085dad59fdd166392201'

headers={
    'Host': 'music.163.com',
    'Origin': 'http://music.163.com',
    'Referer': 'http://music.163.com/song?id=457207812',
    'Save-Data': 'on',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

data={
    'params': '3sdgg68axEngUrM6UAXVWB1Amafsm73X01gYV360JnLyWu+m8f2jDjCX3G4J+PSAl8/vpDitlwclg7qEcGluG/0N29ptCjsSiULEZIKZJ+e3ICSq02nN3N3vIsLCh5foP2pxL4rrSl9aTwhNbv6T86FLqdKU548W4yMHCkAH6Ol280o3l8IOVh6cSwVQ4mil+knCPE1+eix7Ao4oVw85Kheg7ua0vHF+dSCDm5SAr08=',
    'encSecKey': 'a666de5873e039475cdbe089ae33eec9ab0aae66a3906fd7b39356829760b1bda064d0f197923315fc20e62fa5ee1dd0ad87fa2fb75073965a700137bf39c85d80a7d78fba697f35680c0d530d44572c4614e8fda7e6b320f36d8b4a16b4049fb22dc13c1798690301731ff1f940ff9fcfc639e601a9a9688085136a03c91002'
}

def get_page(url):
    s=Session()
    try:
        r=s.post(url,headers=headers,data=data)
        r.raise_for_status()
        r.encoding="utf-8"
        return r.json()
    except Exception as e:
        print("ERROR : ",e.args)

def get_review(json):
    try:
        if json:
            items=json.get('comments')
            for item in items:
                review={}
                review['content']=pq(item['content']).text()
                review['nickname']=pq(item['user']['nickname']).text()
                review['likedCount']=item['likedCount']
                Time=time.localtime(item['time']/1000)
                review['time']=time.strftime("%Y-%m-%d %H:%M:%S",Time)
                yield review

    except Exception as e:
        print(e.args)





def save_MongoDB(dict):
    try:
        db = client.test

        collection = db.netease

        result=collection.insert(dict)

        print('pass',result)
    except Exception as e:

        print(e.args)


def main():
    json=get_page(url)
    for review in get_review(json):
        print(review)
        save_MongoDB(review)

if __name__ == '__main__':
    main()