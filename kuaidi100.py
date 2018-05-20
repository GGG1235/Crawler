
import requests
from urllib.parse import urlencode
import json
from requests import Session
import time

headers={
    'Host': 'www.kuaidi100.com',
    'Referer': 'http://www.kuaidi100.com/',
    'Save-Data': 'on',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

url_type="http://www.kuaidi100.com/autonumber/autoComNum?"
url_message="http://www.kuaidi100.com/query?"

def get_type(num:int):
    s=Session()
    params={
        'resultv2' : '1' ,
        'text' : num
    }
    url=url_type+urlencode(params)

    try:
        r=requests.post(url,headers=headers,timeout=60)
        r.raise_for_status()

        r.encoding=r.apparent_encoding

        json_type=json.loads(r.text).get('auto')

        for i in json_type:
            comCode=i['comCode']
            if comCode is not None:
                yield comCode
            else:
                pass
        pass
    except Exception as e:
        print("ERROR : ",e.args)

def get_message(type:str,num:int):

    params={
        'type' : type ,
        'postid' : num
    }

    url=url_message+urlencode(params)
    try:
        r=requests.get(url,headers=headers,timeout=60)
        r.raise_for_status()
        r.encoding=r.apparent_encoding

        json_message=json.loads(r.text)

        if json_message['message'] != 'ok':
            dict={}
            dict['type']=json_message['message']

            yield dict
        else:
            dict = {}
            items=json_message.get('data')

            for item in items:
                dict['time']=item['time']
                dict['context']=item['context']
                yield dict
    except Exception as e:
        print("ERROR : ",e.args)

def main():
    try:
        num=input("请输入快递单号 : ")
        with open('kuaidi100.log','a+') as f:
            f.write(str(num)+' '+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+'\n')
            f.close()

        print()
        type=get_type(int(num)).__next__()

        for i in get_message(str(type),int(num)):
            print(i['time'],'\n',i['context'])

    except Exception as e:
        print("ERROR : ",e.args)

if __name__ == '__main__':
    main()