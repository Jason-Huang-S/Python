from bs4 import BeautifulSoup as B
import requests as R
import time, re
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

def getdate(url):
    html = get_page(url)
    html = B(html, "html.parser")
    """取得今天的文章"""
    #date 放在 <div class="date">
    dates = html.find_all("div", class_="date")
    for date in dates:
        if "8/28" not in date.text:
            return False
        else:
            return True

def get_content(html):
    html = B(html, "html.parser")
    push = int(input("輸入該文章至少要得到的推文數：\n")) #推文數設定
    """得到上一頁"""
    #上一頁的網址放在 <div class = "btn-group btn-group-paging">

    pre_pages = html.find("div", class_ ="btn-group btn-group-paging")

    pre_pages = pre_pages.find_all("a")
    #從上面資料找"a"，結果會有4個，選我們要的那個
    rule = re.compile(r"\d\d\d\d\d")
    url = pre_pages[1].get("href")
    number = rule.search(url) #從資料中只取出數字 也就是當頁的數字
    number = number.group()


    while True:
        time.sleep(0.2)
        #每次都要造訪：https://www.ptt.cc/bbs/Gossiping/index?????.html，直到文章不是今天為止。
        
        url = "https://www.ptt.cc/bbs/Gossiping/index" + str(number) + ".html"

        if getdate(url) == True: #代表此url列表的文章是 8/28的
            temptitle = get_titles(url,push)
            #temptitle是一個list    
            for title in temptitle:
                print(title)


            number = int(number)
            number = number -1
        else:
            break


def get_titles(url, Repush):
    """取得每篇標題"""
    html = get_page(url)
    html = B(html, "html.parser")
    #先取得該url的html資料
    temptitle = []
    #暫時存放每個title的資料
    
    titles = html.find_all("div", class_ = "title")
    #每篇標題在 <div class="title"> 內 


    """取得推文數超過Repush的文章"""
    #推文數在 <div class="nerc">
    pushs = html.find_all("div", class_="nrec")
    i = 0
    for push in pushs:
        if push.text.isdigit() and int(push.text) >= Repush:
            try:
                temptitle.append(titles[i].text.strip())
            except:
                #如果文章被刪掉，會不能找到標籤 <a> 所以用except跳過
                pass
        i = i +1
    return temptitle

    #回傳整個list



def get_webpages():
    """取得每篇網址"""
    #網址在 <div class>的<a href="">內
    urls = html.find_all("div", class_="title")
    for url in urls:
        time.sleep(0.2)
        # url的資料會是下面這樣
        # <div class="title">
        # <a href="/bbs/Gossiping/M.1630076584.A.ADD.html">Fw: [公告] 8/31 停機公告</a>
        # </div>
        #所以我們從標籤div下面找到標籤a，從標籤a中，用get()函數去取得href所指的網址
        print("https:" + url.a.get('href'))


                  







get_content(get_page("https://www.ptt.cc/bbs/Gossiping/index.html"))



