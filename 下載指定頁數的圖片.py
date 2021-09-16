
import requests as R
from bs4 import BeautifulSoup 
import os
import re
import time
import urllib.request #下載圖片

def get_page(url):
    #得到page
    headers = {"user-agent" : 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }
    resp = R.get(url, headers = headers)
    if resp.status_code != 200:
        print("NG")
        quit()
    return resp.text

def download(url,name):
    #下載圖片用
    urllib.request.urlretrieve(url,"xkcd\\" + name)
    print("Processing:%s..." %name)
    time.sleep(1)
if __name__ == "__main__":

    number = int(input("請輸入下載圖片數量\n"))
    if not os.path.exists("xkcd"): #判斷資料夾是否存在
        os.mkdir("xkcd")

    html = get_page("https://xkcd.com/") #第一次先用https://xkcd.com/ 來找最新網址篇數
    pars = BeautifulSoup(html,"html.parser")
    latest_url = pars.find("meta", property ="og:url").get("content") #這裡存放最新的文章篇數

    #利用正規表達法來取得最新數字-----------
    rule = re.compile(r"\d\d\d\d")  #re
    latest_number = rule.search(latest_url)
    temp_number = int(latest_number.group())
    #---------------------------------

    for i in range(number): #利用下載次數來求文章篇數
        temp_number = temp_number - i 
        #每次都扣i 往前瀏覽 例如: 2565 - 1 = 2564 // 2565 -2 = 2563...
        html = get_page("https://xkcd.com/" + str(temp_number)) #接下來用得到的數字開始做迴圈
        pars = BeautifulSoup(html,"html.parser")
        pic_link = pars.find("div", id="comic").find("img").get("src")
        pic_link = "http:" + pic_link
        #取得連結
        rule = re.compile(r"s/(.*)") #取得圖檔名稱
        temp = rule.search(pic_link)
        pic_name = temp.group()[2:]
        #取得圖檔名稱
        download(pic_link, pic_name)




