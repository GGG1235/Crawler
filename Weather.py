
import json
import requests
from urllib.parse import quote
from tkinter import messagebox
from tkinter import *

headers={
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/52.0.2746.116 Safari/537.36'
}


class Weather:
    def __init__(self):
        self.window = Tk()
        self.window.title("学号:XXXXXXXXX 姓名:XXXXXXXXXX")
        self.window.geometry('1000x800+500+200')

        self.ButtonWeather = Button(self.window, text="查询", command=self.GetString, activebackground="grey", width=10, height=2).place(x=700, y=175)

        e = StringVar()
        self.EN = Entry(self.window, textvariable=e, width=20)
        e.set('0')
        self.EN.place(x=500, y=200)

        self.LabelText = Label(self.window, bg='white', height=15, width=50)
        self.LabelText.place(x=100, y=100)

        self.Label_1 = Label(self.window, bg='white', height=15, width=30)
        self.Label_1.place(x=30, y=400)

        self.Label_2 = Label(self.window, bg='white', height=15, width=30)
        self.Label_2.place(x=250, y=400)

        self.Label_3 = Label(self.window, bg='white', height=15, width=30)
        self.Label_3.place(x=470, y=400)

        self.Label_4 = Label(self.window, bg='white', height=15, width=30)
        self.Label_4.place(x=690, y=400)

        self.window.mainloop()


    def get_weather_data(self):
        url = 'http://wthrcdn.etouch.cn/weather_mini?city=' + quote(self.city_name)
        weather_dict=None
        try:
            weather_data = requests.get(url,headers=headers,timeout=30)
            weather_data.raise_for_status()
            weather_data.encoding = weather_data.apparent_encoding
            weather_dict = json.loads(weather_data.text)
        except Exception as e:
            print(e.args)
        finally:
            self.weather_dict=weather_dict

    def show_weather(self):
        weather_dict = self.weather_dict
        if weather_dict.get('desc') == 'invilad-citykey':
            String = "您输入的城市名有误,或者天气中心未收录您所在的城市"
            messagebox.showinfo("出错了", String)
        elif weather_dict.get('desc') == 'OK':
            forecast = weather_dict.get('data').get('forecast')
            String='城市：'+weather_dict.get('data').get('city')+'\n'+'温度：'+weather_dict.get('data').get('wendu') + '℃ '+'\n'+'风向：'+forecast[0].get('fengxiang')+'\n'+'风级：'+ forecast[0].get('fengli')+'\n'+'高温：'+ forecast[0].get('high')+'\n'+'低温：'+ forecast[0].get('low')+'\n'+'天气：'+ forecast[0].get('type')+'\n'+'日期：'+forecast[0].get('date')+'\n'+'温馨提示：'+weather_dict.get('data').get('ganmao')
            self.LabelText.config(text=String,justify = 'left',wraplength=180,bg='orange')

    def show_weather_ex(self):
        weather_dict = self.weather_dict
        forecast = weather_dict.get('data').get('forecast')
        for i in range(1,4+1):
            String='日期：'+forecast[i].get('date')+'\n'+'天气：'+forecast[i].get('type')+'\n'+'风向：', forecast[i].get('fengxiang')+'\n'+'风级：'+forecast[i].get('fengli')+'\n'+'高温：'+forecast[i].get('high')+'\n'+'低温：'+forecast[i].get('low')
            if(i==1):
                self.Label_1.config(text=String, justify='left', wraplength=180, bg='pink')
            elif(i==2):
                self.Label_2.config(text=String, justify='left', wraplength=180, bg='white')
            elif(i==3):
                self.Label_3.config(text=String, justify='left', wraplength=180, bg='green')
            else:
                self.Label_4.config(text=String, justify='left', wraplength=180, bg='blue')

    def GetString(self):
        self.city_name=""
        Str = self.EN.get()
        self.city_name=Str
        self.get_weather_data()
        self.show_weather()
        self.show_weather_ex()




def main():
    weather=Weather()


if __name__ == '__main__':
    main()