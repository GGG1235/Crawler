import requests
from bs4 import BeautifulSoup as BS
import socket

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/52.0.2746.116 Safari/537.36'
}

def getIPText(url="https://ip.cn/"):
    try:
        r=requests.get(url,headers=headers,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding

        return r.text
    except Exception as err:
        print(str(err))

def getIP(html):
    splt="\t您的内网 IP：{}\n\t您的外网 IP：{}\n\t所在地理位置：{}\n\t{}"
    try:
        soup=BS(html,'lxml')
        GeoIP=soup.find_all(['p'])
        list=soup.find_all(['code'])
        print(splt.format(socket.gethostbyname(socket.gethostname()),list[0].text,list[1].text,GeoIP[len(GeoIP)-2].text))
    except Exception as err:
        print(str(err))

if __name__ == '__main__':
    getIP(getIPText())
