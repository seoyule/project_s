import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from unicodedata import normalize
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

# 신상마켓 로그인
driver.get('https://sinsangmarket.kr/login')
try:
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div/div[2]/div[3]/p').click()
except:
    pass
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[1]/input').click()
action.send_keys('protestt').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[2]/input').click()
action.send_keys('!QAZwsx123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button').click()
print("신상 로그인 성공")

# 광고 있으면 close
time.sleep(.5)
try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass

# 한글로 바꾸기
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/div').click()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/ul/li[1]/label').click()
time.sleep(.5)

# 광고 있으면 close
try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass

# cafe24 열기
driver.execute_script('window.open("https://eclogin.cafe24.com/Shop/");')
driver.switch_to.window(driver.window_handles[1])
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

#테이블 정보 추출
table_MN = pd.read_html(driver.page_source, match = '주문번호')
df = table_MN[1]

"""admin_ = df[df['상품명/옵션'] =='USER  ADMIN'].index
df.drop(admin_, inplace=True)"""
df = df[df['상품명/옵션'] != 'USER  ADMIN']

df['주문번호'] = df['주문번호'].replace('(\S+)\s+.*',r'\1', regex=True)
df['주문자'] = df['주문자'].replace('(.*)\s\sSMS.*',r'\1', regex=True) #송정애  SMS  [비회원] 뒤 SMS 등 제거
df['상품명/옵션'] = df['상품명/옵션'].replace('상품 상세보기  쇼핑몰화면 진열보기  내역  (.*)',r'\1', regex=True)
df.drop(['묶음선택','Unnamed: 4','운송장정보','공급사','결제수단','메모','총 실결제금액'], axis=1, inplace= True)

#상품코드 따기
search = []
for values in df['상품명/옵션']:
    try:
        code = re.search(r'\([A-Z0]{8}\)', values).group()
    except:
        code = "N/A"
    search.append(code)
df['code'] = search

#상품제목 따기
search = []
for values in df['상품명/옵션']:
    try:
        title = re.search(r'(.*)\([A-Z0]{8}\)', values).group(1)
    except:
        title = "N/A"
    search.append(title)
df['title'] = search

#link 따기
search = []
for values in df['상품명/옵션']:
    try:
        title = re.search(r'.*(https.*)\s\s색상', values).group(1)
    except:
        title = "N/A"
    search.append(title)
df['link'] = search


"""
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df)
    """
#df.to_excel("/Users/seoyulejo/Downloads/output.xlsx")