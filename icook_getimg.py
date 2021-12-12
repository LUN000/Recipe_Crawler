from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import os
import time
from tqdm import tqdm

def getsoup(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43'
            }
    response = requests.get(url,headers=header)
    soup = BeautifulSoup(response.text,"html.parser")
    return response, soup


food = input('輸入食物: ')
url_icook = f"https://icook.tw/search/{food}"
response_icook, soup_icook = getsoup(url_icook)

flag = True
pages = 1
datas =[]
#取得各頁
while flag:
    div_icook = soup_icook.find_all(class_="browse-recipe-item")
    for tag in div_icook:
        img_link = tag.find('img')['data-src']
        datas.append(img_link)
    #下一業
    try:
        pages += 1
        page_flag = eval(soup_icook.find_all('a', class_="pagination-tab-link--number")[-1].text)-1
        if pages>page_flag:
            flag = False
        else:    
            url_icook = f"https://icook.tw/search/{food}/?page={pages}"
            print(url_icook)
            response_icook, soup_icook = getsoup(url_icook)
    except:
        print('Error1')
        flag = False
        
#取得最後一頁
url_icook = f"https://icook.tw/search/{food}/?page={pages}"
print(url_icook)
response_icook, soup_icook = getsoup(url_icook)
div_icook = soup_icook.find_all(class_="browse-recipe-item")
for tag in div_icook:
    img_link = tag.find('img')['data-src']
    datas.append(img_link)

#下載圖片
process = tqdm(range(len(datas)))
for index, link in enumerate(datas):
    if not os.path.exists(f"{food}imgs"):
        os.mkdir(f"{food}imgs")  # 建立資料夾
    process.update(1)
    img = requests.get(link)  # 下載圖片
    with open(f"{food}imgs\\" + food + str(index+1) + ".jpg", "wb") as file:  # 開啟資料夾及命名圖片檔
        file.write(img.content)  # 寫入圖片的二進位碼
print('Finish')

