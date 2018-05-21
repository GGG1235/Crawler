
import requests
import re
import os 

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
     
def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price , title])
    except:
        print("")
 
def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
         
def connect(goods,depth):
    start_url = 'http://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)
     
def main():
    while True:
        os.system("cls")
        goods=input("请输入您要查询的商品 : ")
        depth=input("请输入您要查看的页数 : ")

        if goods=="" or depth=="" or (goods=="" and depth=="") or (ord(depth)>57 or ord(depth)<48):
            print("请正确输入 ！！！")
        else:
            connect(goods,int(depth))

        booth=input("是否继续查询(Y/N)? ")
        if booth=='y' or booth=='Y':
            os.system("cls")
        elif booth=='n' or booth =='N':
            os.system("cls")
            break
        else:
            os.system("cls")
            print("请正确输入！！！")


if __name__=="__main__":
    main()