利用https://ipstack.com/所提供的方式來查找ip位址，只能查到城市。
![image](https://github.com/Jason-Huang-S/Python-web-crawler/blob/main/%E9%80%8F%E9%81%8Eip%E4%BE%86%E6%9F%A5%E6%89%BE%E6%AD%A4ip%E5%9F%8E%E5%B8%821.png)



import requests as R
from bs4 import BeautifulSoup 
import re
def get_page(url):
    headers = {"cookie":"over18=1" , 
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    #在使用get的時候，通常會傳入headers，我們將headers裡面的cookie增加over18 = 1 來讓網頁覺得我們已經over18
    #user-agent可加可不加
    Get = R.get(url, headers = headers)

    if Get.status_code != 200:
        print("無法連線，status code:", Get.status_code)
        quit()
    elif "未滿18" in Get.text:
        print("無法連線，因為未滿18")
        quit()
    else:
        return(Get.text)

def get_url(html):
    """取得各個文章的url"""
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("div", class_="title")
    sortedlinks = []
    for link in links:
        try:#避免文章被刪掉找不到網址
            if "href" in link.a.attrs: 
                sortedlinks.append("https://www.ptt.cc" + link.a.get("href")) #取得網址，放入list
        except:
            pass
    return sortedlinks

def get_ips(文章內文):
    """取得發文者的ip"""
    #html裡面會有  發信站: 批踢踢實業坊(ptt.cc), 來自: 122.121.41.28 (臺灣) 
    #可以透過 \d+\.\d+\.\d+\.\d+ 正規表達法去搜尋到ip位置

    rule = re.compile(r"\d+\.\d+\.\d+\.\d+") #定義正規表達的規則
    ip = re.search(rule, 文章內文) #從文章內文中搜尋ip
    if ip != "":
        ip = ip.group()
        return(ip)
    else:
        print("無法搜尋到ip")

def get_country(ips):
    """
    利用ip.stack網站所提供的功能，輸入ip就可得到ip使用者的國家位置，需要載入API。
    ip.stack會回傳json檔案，所以我們要用json檔案來分析，json其實很像python裡面的dict
    用法是http://api.ipstack.com/[IP位置]?access_key=[API的鑰匙]
    """
    if ips != "":
        API_KEY = "API CODE"
        url = "http://api.ipstack.com/" + ips + "?access_key=" + API_KEY
        data = R.get(url).json()
        #取得網址後，將資料轉成json檔案

        city = data["city"]
        #取出city的資料
    return(city)
url = "https://www.ptt.cc/bbs/Gossiping/index.html"
html = get_page(url)
links = get_url(html) #取得各個文章的連結

for link in links: #進入各個文章的連結 取得文章內容
    文章內文 = get_page(link) #取得文章內容
    ip = get_ips(文章內文)
    print("文章連結：", link, "此人住在：", get_country(ip))
