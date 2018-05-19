
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq

headers={
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/3660392817',
    'Save-Data': 'on',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

initial_url="https://m.weibo.cn/api/container/getIndex?"

def get_page(page):
    params={
        'type':'uid',
        'value':'3660392817',
        'containerid':'1076033660392817',
        'page':page
    }

    url=initial_url+urlencode(params)

    try:
        r=requests.get(url,headers=headers,timeout=60)
        r.raise_for_status()

        r.encoding=r.apparent_encoding
        return r.json()
    except Exception as err:
        print("ERROR",err.args)

def parse_page(json):
    try:
        if json:
            items=json.get('data').get('cards')
            for item in items:
                weibo={}
                weibo['time']=item.get('mblog')['created_at']
                weibo['text']=pq(item.get('mblog')['text']).text()
                weibo['attitudes'] = item.get('mblog')['attitudes_count']
                weibo['comments'] = item.get('mblog')['comments_count']
                weibo['reposts'] = item.get('mblog')['reposts_count']
                yield weibo
        else:
            return
    except Exception as err:
        print(str(err))

def main():
    try:
        for i in range(1,9):
            json=get_page(i)
            for weibo in parse_page(json):
                for keys in weibo.keys():
                    print(keys,':',weibo[keys])
                print()
            print()
    except Exception as err:
        print(str(err))

if __name__ == '__main__':
    main()