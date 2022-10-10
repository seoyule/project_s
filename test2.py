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
import zipfile
import glob
import os

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
driver.switch_to.new_window('tab')
time.sleep(.5)
driver.switch_to.window(driver.window_handles[1])
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

#엑셀 다운로드
driver.find_element_by_xpath('//*[@id="eExcelDownloadBtn"]').click()
time.sleep(1)
driver.switch_to.window(driver.window_handles[2])

select = Select(driver.find_element_by_xpath('//*[@id="aManagesList"]'))
select.select_by_visible_text('ForOrderSejo')
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="Password"]').click()
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="PasswordConfirm"]').click()
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="QA_common_password1"]/div[3]/a').click() #자료 요청
time.sleep(.5)

alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[2])

time.sleep(10)
driver.find_element_by_xpath('//*[@id="QA_common_password2"]/div[3]/table/tbody/tr[1]/td[7]').click() #다운로드 버튼

driver.find_element_by_xpath('//*[@id="password"]').click() #다시 비밀번호 물어봄
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="reason_for_download"]').click() #이유 적어줌
action.send_keys('analysis').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="excel_download"]').click() #파일요청
time.sleep(7)
driver.close()
driver.switch_to.window(driver.window_handles[1])

#다운로드 zip 파일 이름 확인 https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
search_dir = "/Users/seoyulejo/Downloads/"
files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_path = files[-1]

#zip 풀기
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall('/Users/seoyulejo/Downloads/', pwd=b'protest123')

#변환 파일 이름 확인 https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
search_dir = "/Users/seoyulejo/Downloads/"
files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name = files[-1]

df = pd.read_csv(file_name)

df['option1'] = df['상품옵션'].replace('.*=(\S+),.*',r'\1', regex=True)
df['option2'] = df['상품옵션'].replace('.*=.*=(.*)',r'\1', regex=True)
title_ss = []
price_ss = []
shop_name = []
building_name = []
shop_location = []
shop_phone_number = []
note = []

for i in range(len(df)):
    link = df['모델명'][i]
    driver.switch_to.new_window('tab')
    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])
    try:
        driver.get(link)
        time.sleep(1.5)
    except:
        note.append('!! url 없음 !!')
        title_ss.append('!! url 없음 !!')
        price_ss.append('!! url 없음 !!')
        shop_name.append('!! url 없음 !!')
        building_name.append('!! url 없음 !!')
        shop_location.append('!! url 없음 !!')
        shop_phone_number.append('!! url 없음 !!')

        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(.5)
        continue
    #품절확인
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #도매상품이름
    title = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/p').text
    if soup.find("div", attrs={'class': 'sold-out'}):
        note.append('!! sold-out !!')
    else:
        title_ss.append(title)
        note.append('OK')
    title_ss.append(title)
    time.sleep(.5)
    #도매가격
    price = int(driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/span').text.replace(",",""))
    price_ss.append(price)
    time.sleep(.5)

    #가게 화면 진입
    driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').click()
    time.sleep(1.5)
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(.5)
    #가게이름
    shop_n = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/span').text
    shop_name.append(shop_n)
    time.sleep(.5)
    #전화번호
    shop_p = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div').text.strip()
    shop_phone_number.append(shop_p)
    time.sleep(.5)

    address = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div').text.strip()
    #빌딩이름
    try:
        building_n = re.search(r'(.*)\s\S+층\s.*', address).group(1)
    except:
        try:
            building_n = re.search(r'(.*\s별관)\s.*', address).group(1)
        except:
            building_n = address
    building_name.append(building_n)
    time.sleep(.5)
    #주소
    try:
        shop_l = re.search(r'.*\s(\S+층\s.*)', address).group(1)
    except:
        try:
            shop_l = re.search(r'.*\s별관\s(.*)', address).group(1)
        except:
            shop_l = address
    shop_location.append(shop_l)
    time.sleep(.5)

    driver.close()
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    print(i+1,"완료")

df['title_ss'] = title_ss
df['price_ss'] = price_ss
df['shop_name'] = shop_name
df['building_name'] = building_name
df['shop_location'] = shop_location
df['shop_phone_number'] = shop_phone_number
df['note'] = note

cols = df.columns.tolist()
cols = cols[:10]+cols[11:13]+cols[14:17]+cols[10:11]+cols[13:14]+cols[17:]
df = df[cols]

timestr = time.strftime("%Y%m%d")
df.to_excel("/Users/seoyulejo/Downloads/files/order_master_"+timestr+".xlsx")

df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','shop_location', 'shop_phone_number','모델명'],dropna=False)[['수량']].sum()
df2.to_excel("/Users/seoyulejo/Downloads/files/order_form_"+timestr+".xlsx", index=False)


#반품재고와 비교
df['temp_key'] = df.apply(lambda row: row.colC + row.colE, axis=1)


#timestr = time.strftime("%Y%m%d-%H%M%S")
#
#new_file_name = "order_master_"+timestr
#os.rename(file_name, "/Users/seoyulejo/Downloads/"+new_file_name)



