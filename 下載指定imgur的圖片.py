
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
    urllib.request.urlretrieve(url,"imgur\\" + name)
    print("Processing:%s..." %name)
    time.sleep(1)

if __name__ == "__main__":

    url = "https://imgur.com/search/score?q="

    searchname = input("請輸入要搜尋的圖片tag\n")
    if not os.path.exists("imgur"): #判斷資料夾是否存在
        os.mkdir("imgur")

    html = get_page(url + searchname) 

    pars = BeautifulSoup(html,"html.parser")

    #每篇圖片放在<a class="image-list-link" href="/gallery/TWKOjMF" data-page="0">
    #           <img alt="" src="//i.imgur.com/TWKOjMFb.jpg" />
    imgs = pars.find_all("a", class_ ="image-list-link")
    for img in imgs:
        img_link = "https:" + img.find("img").get("src")
        #取得link

        rule = re.compile(r"m/(.*)")
        temp_name = rule.search(img_link)
        name = temp_name.group()[2:]
        #取得各個圖檔名稱

        download(img_link,name)
    print("done")





