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


# 기본-cafe24: 상품목록 진입
driver.get('https://soyool.cafe24.com/disp/admin/shop1/product/productmanage')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="eBtnSearch"]').click()  # 조회버튼 클릭
time.sleep(1)

# 기본-cafe24: 상품 목록 출력
num_goods = driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[1]/p').text
num_goods = int(num_goods.split(" ")[1].split("개")[0])
looping_num = num_goods / 100
looping_num = math.ceil(looping_num)

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

# 기본-cafe24: 공급사 보이게
driver.find_element_by_xpath('//*[@id="QA_list2"]/div[3]/div[3]/div/a/span').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="listSubject"]/div[1]/ul/li[15]/label').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="eColumnApply"]/span').click()
time.sleep(2)

start_loop = 20
start_item = 0

if start_loop != 0:
    a = start_loop//10 #몇번 다음페이지 그룹을 눌러야 하는지
    if a>0:
        for i in range(a):
            for n in range(20):
                action.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(.5)
            element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a')
            action.move_to_element(element)
            element.click()
            time.sleep(2)
            driver.refresh()

for loop in range(start_loop,looping_num):
    if loop%10 == 0 and loop != start_loop: #next page 그룹버튼 누르기
        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a')
        action.move_to_element(element)
        element.click()
        time.sleep(3)

    if loop != start_loop:
        driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop%10 + 1}]').click()  # 페이지 번호버튼 클릭
        time.sleep(3)

    if loop == looping_num-1:
        num = num_goods - (looping_num-1)*100
    else:
        num = 100
    time.sleep(1)

    if loop == start_loop:
        start= start_item
    else:
        start=0
    time.sleep(1)

    if loop == start_loop:
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)

    for i in range(start,num):

        #첫번째 아이템 클릭
        time.sleep(1)
        pyautogui.press('ctrl')  # sleep 방지
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, f'//*[@id="product-list"]/tr[{i+1}]/td[5]/div/p/a')))
        element = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i+1}]/td[5]/div/p/a')
        action.move_to_element(element).perform()
        subject = element.text
        print(subject)
        element.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1.5)

        try:
            #정보 확보
            time.sleep(.5)
            element1 = driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[4]/td/input')
            ele1 = element1.get_attribute("value")
            time.sleep(.5)

            element2 = driver.find_element_by_xpath('//*[@id="eProductModelName"]')
            ele2 = element2.get_attribute("value")
            time.sleep(.5)

            element3 = driver.find_element_by_xpath('//*[@id="ma_product_code"]')
            time.sleep(.5)

            #데이터 교체
            if "http" in ele1:
                link = ele1
                seller = ele2

            else:
                link = ele2
                seller = ele1

            element1.clear()
            element1.send_keys(seller," ",link)
            time.sleep(.5)

            element2.clear()
            element2.send_keys(link)
            time.sleep(.5)

            element3.send_keys(seller)
            time.sleep(.5)

            driver.find_element_by_xpath('//*[@id="eProductModify"]').click() #저장
            time.sleep(1.5)
            alert = driver.switch_to.alert
            time.sleep(.7)
            alert.accept()
            time.sleep(.5)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(3)
            print(loop+1,"-",i+1,"번째 완료")

        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(loop + 1, "-", i + 1, "번째 실패")
            time.sleep(2)

