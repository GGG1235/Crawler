import requests
from requests import Session
import re
from urllib.request import quote
import os
import getpass

headers={
    'host': 'www.toutiao.com',
    'referer': 'https://www.toutiao.com/search/?keyword={keyword}',
    'save-data': 'on',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

initial_url='https://www.toutiao.com/search_content/?offset={offset}&format=json&keyword={keyword}&autoload=true&count=20&cur_tab=1&from=search_tab'

s=Session()

def get_offset(offset,Keyword):
    keyword=quote(Keyword)

    headers['referer']=headers['referer'].format(keyword=keyword)

    url=initial_url.format(offset=offset,keyword=keyword)

    try:
        r=s.get(url,headers=headers,timeout=60)
        r.raise_for_status()
        r.encoding=r.apparent_encoding

        return r.json()
    except Exception as err:
        print("ERROR : ",str(err))

def getimage_list(json):
    try:
        if json:
            image_lists=json.get('data')
            for image_list in image_lists:
                images=image_list.get('image_list')
                if images not in [None,[]]:
                    for image in images:
                        image_url="http:"+image['url']
                        image_url_next=re.sub('/list/','/origin/',image_url)
                        yield image_url_next
                else:
                    pass
        else:
            return
    except Exception as err:
        print("ERROR : ",str(err))


def download_image(image_url,keyword):
    user=getpass.getuser()
    root = "C:/Users/{user}/Desktop/{keyword}//".format(user=user,keyword=keyword)
    path = root + image_url.split('/')[-1]+'.jpg'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r=requests.get(image_url,headers={'User-Agent':'Mozilla/5.0'})
            with open(path,'wb') as f:
                f.write(r.content)
                f.close()
                print(image_url.split('/')[-1],"下载完成")
        else:
            print("文件已存在")
    except:
        print("抓取失败")

def main():
    try:
        Keyword=input()
        for i in range(1,5):
            json=get_offset(offset=i*20,Keyword=Keyword)
            for i in getimage_list(json):
                download_image(i,Keyword)
    except Exception as e:
        print("ERROR : ",e.args)

if __name__ == '__main__':
    main()
