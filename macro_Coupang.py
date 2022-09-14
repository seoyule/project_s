# for 변수: k,j,i
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

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
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
time.sleep(1)
print("cafe24 진입")

driver.get('https://mp.cafe24.com/mp/main/front/service')
time.sleep(1)
print("마켓플러스 진입")

# 기본-cafe24: 상품목록 진입
driver.get('https://mp.cafe24.com/mp/product/front/manageList')
time.sleep(1)
print("상품목록 진입")

# 기본-cafe24: 승인 대기만 선택
num_goods = driver.find_element_by_xpath('//*[@id="stats_status_wait_count"]/span').click()
time.sleep(1)

# 기본-cafe24: 쿠팡 선택
select = Select(driver.find_element_by_xpath('//*[@id="search_category_market"]'))  # 검색종류
select.select_by_visible_text('쿠팡')
time.sleep(1)

#검색버튼 클릭
num_goods = driver.find_element_by_xpath('//*[@id="manage_search_frm"]/div/div/div[2]/button').click()
time.sleep(1)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

#전체선택
driver.find_element_by_xpath('//*[@id="product_list"]/div/div[1]/table/thead/tr/th[1]/div/label/input').click() # 이미지 개별 전환
time.sleep(.5)

#승인상태 동기화
driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[2]/div/div[1]/div[1]/div/div/button[1]').click() # 이미지 개별 전환
time.sleep(.5)

#확인
wait.until(EC.alert_is_present())
time.sleep(.5)
alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[0])
time.sleep(.5)
print("승인상태 동기화 됨")

#################################################
### 승인반려 - 사진 크기 조절

# 기본-cafe24: 승인 반려만 선택
num_goods = driver.find_element_by_xpath('//*[@id="stats_status_reject_count"]/span').click()
time.sleep(1)

# 기본-cafe24: 쿠팡 선택
select = Select(driver.find_element_by_xpath('//*[@id="search_category_market"]'))  # 검색종류
select.select_by_visible_text('쿠팡')
time.sleep(1)

#검색버튼 클릭
num_goods = driver.find_element_by_xpath('//*[@id="manage_search_frm"]/div/div/div[2]/button').click()
time.sleep(1)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

# 기본-cafe24: 상품 목록 출력
num_goods = driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[1]/span/strong').text
num_goods = int(num_goods)
looping_num = num_goods / 100
looping_num = math.ceil(looping_num)
print(num_goods, "개 아이템")

for j in range(num_goods):  # 설정하기
    print(j+1, "번째아이템 시작")

    # 신상: 아이템 클릭 (첫번째 창)
    pyautogui.press('ctrl')  # sleep 방지
    time.sleep(1)
    element = driver.find_element_by_xpath(f'//*[@id="eMultiTable"]/tbody/tr[1]/td[7]/div/a')
    action.move_to_element(element).perform()
    element.click()
    time.sleep(1)

    # 아이템 창으로 들어옴
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="QA_register_product"]/div[2]/table/tbody/tr[2]/td[1]/label/span').click() # 이미지 개별 전환
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="imgRegisterContainer"]/ul/li/span[3]/a[2]/span').click() # 자르기 클릭
    time.sleep(1)
    action.send_keys(Keys.PAGE_DOWN).perform()
    element = driver.find_element_by_xpath('//*[@id="layerMarketImageEditor"]/div[2]/a[1]/span')
    action.move_to_element(element).perform()
    element.click()
    time.sleep(.5)
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath('//*[@id="footer"]/a[7]/span').click()
    time.sleep(1)

    wait.until(EC.alert_is_present())
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


####################################################
### 승인 대기중인거 다시 현재 상태 확인으로...

# 기본-cafe24: 승인 대기만 선택
num_goods = driver.find_element_by_xpath('//*[@id="stats_status_wait_count"]/span').click()
time.sleep(1)

# 기본-cafe24: 쿠팡 선택
select = Select(driver.find_element_by_xpath('//*[@id="search_category_market"]'))  # 검색종류
select.select_by_visible_text('쿠팡')
time.sleep(1)

#검색버튼 클릭
num_goods = driver.find_element_by_xpath('//*[@id="manage_search_frm"]/div/div/div[2]/button').click()
time.sleep(1)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

#전체선택
driver.find_element_by_xpath('//*[@id="product_list"]/div/div[1]/table/thead/tr/th[1]/div/label/input').click() # 이미지 개별 전환
time.sleep(.5)

#승인상태 동기화
driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[2]/div/div[1]/div[1]/div/div/button[1]').click() # 이미지 개별 전환
time.sleep(.5)

#확인
wait.until(EC.alert_is_present())
time.sleep(.5)
alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[0])
time.sleep(.5)

#########################################
### 다시 반려된 거.. 추가 이미지 삭제

# 기본-cafe24: 승인 반려만 선택
num_goods = driver.find_element_by_xpath('//*[@id="stats_status_reject_count"]/span').click()
time.sleep(1)

# 기본-cafe24: 쿠팡 선택
select = Select(driver.find_element_by_xpath('//*[@id="search_category_market"]'))  # 검색종류
select.select_by_visible_text('쿠팡')
time.sleep(1)

#검색버튼 클릭
num_goods = driver.find_element_by_xpath('//*[@id="manage_search_frm"]/div/div/div[2]/button').click()
time.sleep(1)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

# 기본-cafe24: 상품 목록 출력
num_goods = driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[1]/span/strong').text
num_goods = int(num_goods)
looping_num = num_goods / 100
looping_num = math.ceil(looping_num)
print(num_goods, "개 아이템")

for j in range(num_goods):  # 설정하기
    print(j+1, "번째아이템 시작")

    # 신상: 아이템 클릭 (첫번째 창)
    pyautogui.press('ctrl')  # sleep 방지
    time.sleep(1)
    element = driver.find_element_by_xpath(f'//*[@id="eMultiTable"]/tbody/tr[1]/td[7]/div/a')
    action.move_to_element(element).perform()
    element.click()
    time.sleep(1)

    # 아이템 창으로 들어옴
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="QA_register_product"]/div[2]/table/tbody/tr[3]/td[1]/label/span').click() # 추가 이미지 개별 전환
    time.sleep(1)
    action.send_keys(Keys.PAGE_DOWN).perform()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    datas = soup.find_all("li", attrs={'class':'eAddImageRow'})

    for i in range(len(datas)):
        try:
            element = driver.find_element_by_xpath('//*[@id="eExtraImage"]/li[2]/span/img')
            action.move_to_element(element).perform()
            element.click()
            driver.find_element_by_xpath('//*[@id="eExtraImage"]/li[2]/span/button').click()
            time.sleep(.5)
        except:
            pass
    driver.find_element_by_xpath('//*[@id="footer"]/a[7]/span').click()
    time.sleep(1)
    wait.until(EC.alert_is_present())
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


# 기본-cafe24: 승인 대기만 선택
num_goods = driver.find_element_by_xpath('//*[@id="stats_status_wait_count"]/span').click()
time.sleep(1)

# 기본-cafe24: 쿠팡 선택
select = Select(driver.find_element_by_xpath('//*[@id="search_category_market"]'))  # 검색종류
select.select_by_visible_text('쿠팡')
time.sleep(1)

#검색버튼 클릭
num_goods = driver.find_element_by_xpath('//*[@id="manage_search_frm"]/div/div/div[2]/button').click()
time.sleep(1)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

#전체선택
driver.find_element_by_xpath('//*[@id="product_list"]/div/div[1]/table/thead/tr/th[1]/div/label/input').click() # 이미지 개별 전환
time.sleep(.5)

#승인상태 동기화
driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[2]/div/div[1]/div[1]/div/div/button[1]').click() # 이미지 개별 전환
time.sleep(.5)

#확인
wait.until(EC.alert_is_present())
time.sleep(.5)
alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[0])
time.sleep(.5)