import re, os, time
import requests as R
from bs4 import BeautifulSoup as B
import urllib.request #用來下載圖片

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

def parser_image(html):
    """取得網頁中所有imgur的網址"""
    img = B(html, "html.parser")
    links = img.find("div", id="main-content" , class_ = "bbs-screen bbs-content").find_all("a")

    # # 方法一：
    # for link in links:
    #     print(link.get("href"))

    #方法二：
    imglinks = []
    for link in links:
        rule = re.compile(r"http(s)?://(i.)?(m.)?imgur.com/.......")
        imgur = re.search(rule, link.get("href"))
        if imgur != None and imgur.string == link.get("href"):
            imglinks.append(link.get("href"))
    return imglinks #回傳一個list 包含該文章所有的imgur網址

def getdate(url):
    html = get_page(url)
    html = B(html, "html.parser")
    """取得今天的文章"""
    #date 放在 <div class="date">
    dates = html.find_all("div", class_="date")
    #字串處理
    today_time = time.strftime("%m/%d").lstrip("0")
    #字串處理

    for date in dates:
        if today_time in date.text or "8/29" in date.text: #如果文章是今天日期的話
            return True
        else:
            return False

def get_content(html):#回傳所有符合文章的標題 回傳title links

    html = B(html, "html.parser")
    input("要取得的文章日期：\n")
    push = int(input("該文章至少要得到的推文數：\n")) #推文數設定
    """得到上一頁"""
    #上一頁的網址放在 <div class = "btn-group btn-group-paging">

    pre_pages = html.find("div", class_ ="btn-group btn-group-paging")

    pre_pages = pre_pages.find_all("a")
    #從上面資料找"a"，結果會有4個，選我們要的那個
    rule = re.compile(r"\d\d\d\d")
    url = pre_pages[1].get("href")
    number = rule.search(url) #從資料中只取出數字 也就是當頁的數字
    number = number.group() 

    titles =[] #用來儲存所有符合的文章標題
    links = [] #用來存放links 
    while True:
        time.sleep(0.2)
        #每次都要造訪：https://www.ptt.cc/bbs/Beauty/index?????.html，直到文章不是今天為止。
        
        url = "https://www.ptt.cc/bbs/Beauty/index" + str(number) + ".html"

        if getdate(url) == True: #代表此url列表的文章是今日的
            temptitle, templinks = get_titles_links(url,push)
            #temptitle是一個list    
            titles.append(temptitle)
            links.append(templinks)
            number = int(number)
            number = number -1
        else:
            break
    return(titles, links) #回傳所有符合文章的標題

def get_titles_links(url, Repush): #Repush 是要超過的推文數
    """取得每篇標題+links"""
    html = get_page(url)
    html = B(html, "html.parser")
    #先取得該url的html資料
    temptitle = []
    #暫時存放每個title的資料

    templinks = []
    #存放文章的link

    titles_links = html.find_all("div", class_ = "title")
    #每篇標題在 <div class="title"> 內 
    #每篇link放在<div class ="title">內的href

    """取得推文數超過Repush的文章"""
    #推文數在 <div class="nerc">
    pushs = html.find_all("div", class_="nrec")
    i = 0
    for push in pushs:
        if push.text.isdigit() and int(push.text) >= Repush: #如果該文章的推文次數大於repush
            try:
                temptitle.append(titles_links[i].text.strip()) #取得標題
                templinks.append("https://www.ptt.cc"+titles_links[i].a.get("href")) #取得link 放入templinks
            except:
                #如果文章被刪掉，會不能找到標籤 <a> 所以用except跳過
                pass
        i = i +1
    return(temptitle, templinks)
    #回傳整個list 包含links 和 標題

def save_img(imglinks, filename): #用來存檔imgur，要傳入imgur的網址
    if imglinks: #imglinks = list
        i = 0
        for imglink in imglinks: #進入imgur載圖片
            print("Processing", filename, "....")
            i = i +1
            imglink = imglink.strip() #清掉空白
            path = filename + "\\" + str(i) + ".jpg"
            urllib.request.urlretrieve(imglink, path)

if __name__ == "__main__":
    url = "https://www.ptt.cc/bbs/Beauty/index.html"
    html = get_page(url)
    標題s, 連結s = get_content(html) #標題是回傳list 連結是回傳string
    
    allnames = [] #用來防止title錯位

    print("總共取得下列文章\n")
    for dirnames in 標題s:
        for dirname in dirnames:
            print(dirname) #取得各個標題
            time.sleep(0.3)
            if not os.path.isdir(os.getcwd() + "\\" + dirname): #判斷是否存在資料夾
                os.makedirs(os.getcwd() + "\\" + dirname)
            allnames.append(dirname)
    print("開始進行下載...")

    i = 0 #存圖片用的圖片名字
    for links in 連結s:
        for link in links:
            link = link.strip()
            articles_html = get_page(link) #取得符合的文章的html
            img_links = parser_image(articles_html) #將文章的html傳入parser 取得文章內的imgur link
            path = os.getcwd() + "\\" + allnames[i]
            save_img(img_links, path)
            i = i + 1
    print("done")
    #創建資料夾:
