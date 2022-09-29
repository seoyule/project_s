from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
import os
import re
import time
import requests
import pyautogui
import warnings
import shutil
import math
import back_data_mine
from PIL import Image
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


# 기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver") #, options=options
driver.maximize_window()
driver.implicitly_wait(15)
action = ActionChains(driver)
wait = WebDriverWait(driver, 20)

category_list = back_data_mine.category_list # 분류설정

# 기본-cafe24: 열기
driver.get("https://eclogin.cafe24.com/Shop/")
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="mall_id"]').click()
time.sleep(.5)
action.send_keys('soyool').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('!QAZwsx123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(3)
print("cafe24 진입")

driver.get('https://soyool.cafe24.com/admin/php/shop1/s_new/shipped_begin_list.php') #배송준비중으로 이동
time.sleep(2)
driver.find_element_by_xpath('//*[@id="QA_deposit1"]/div[2]/table/tbody/tr[2]/td/a[6]').click() #지난 한달 선택
time.sleep(1)
driver.find_element_by_xpath('//*[@id="search_button"]').click() #검색

# 소스 수집
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

datas = soup.find_all("td", attrs={'class': 'w220 left'})
orders = []

for data in datas:
    link = data.find("p", attrs={'class': 'supply'}).get_text()
    p = re.compile(r'.*(https.*)\n', re.DOTALL)
    m = p.search(link)
    if m == None:
        continue
    link = m.group(1)

    options_r = data.find("ul", attrs={'class': 'etc'})
    options_ = options_r.find_all("li")
    options = []
    for op in options_:
        op = op.get_text()
        p = re.compile(r'.*: (.*)')
        m = p.search(op)
        if m == None:
            continue
        option = m.group(1)
        options.append(option)#옵션 구하기

    orders.append((link,options))
"""
'//*[@id="goods-detail"]/div/div[2]/div[2]/div[2]/ul/li[1]/div/div[1]/div[2]/div[1]' #옵션

'//*[@id="goods-detail"]/div/div[2]/div[2]/div[2]/ul/li[1]/div/div[2]/div/button[1]' #수량 -
'//*[@id="goods-detail"]/div/div[2]/div[2]/div[2]/ul/li[1]/div/div[2]/div/button[2]' #수량 +
'//*[@id="goods-detail"]/div/div[2]/div[2]/div[2]/ul/li[2]/div/div[2]/div/button[2]' #두번째 수량+
"""

