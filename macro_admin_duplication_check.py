# for 변수: k,j,i
from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
import os
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import pyautogui
import warnings
import shutil
import math
import back_data_mine
import pickle
from PIL import Image
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


# 기본세팅
start = 1 # 중간부터 시작 시작 - 개수 번째
number = 500 # 아이템 검색 개수
down_path = '/Users/seoyulejo/Downloads/imgs/'
error = []
n = 0 #완료된 상품 개수
subject_list = [] # 중복상품 체크
subject_4f = ""
existing = 0

warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
driver.maximize_window()
driver.implicitly_wait(15)
action = ActionChains(driver)
wait = WebDriverWait(driver, 15)

category_list = back_data_mine.category_list # 분류설정
with open('listfile', 'rb') as fp: # url 리스트 불러오기
    urls = pickle.load(fp)

# 기본-신상: 신상마켓 로그인
driver.get('https://sinsangmarket.kr/login')

# 기본-cafe24: 열기
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
time.sleep(1)
# 기본-cafe24: 광고 있으면 close
"""try:
    driver.find_element_by_class_name("btnClose.eClose").click()
    time.sleep(.3)
except:
    pass"""
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btnPromodeView')))
#driver.find_element_by_class_name('btnPromodeView').click()# new 관리자 화면 진입 'newPromodeArea
#time.sleep(.5)
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
print("총",num_goods,"개")
print("페이지",looping_num,"개")

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

for i in range(12):
    action.send_keys(Keys.DOWN).perform()

# 기본-cafe24: 공급사 보이게
driver.find_element_by_xpath('//*[@id="QA_list2"]/div[3]/div[3]/div/a/span').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="listSubject"]/div[1]/ul/li[15]/label').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="eColumnApply"]/span').click()
time.sleep(1)

#맨뒤로 가기
books = math.floor(looping_num/10)
for book in range(books): #looping_num
    if book == 0:
        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a')
    else:
        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a[2]')
    action.move_to_element(element).perform()
    element.click()
    time.sleep(1)


# 기본-cafe24: 목록 스크린 (goods_list)
goods_list = []
error_list = []
for loop in reversed(range(looping_num)):  # looping_num
    dup = 0
    if loop % 10 == 9 and loop != looping_num-1:  # next page 버튼 누르기
        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a[1]')
        action.move_to_element(element).perform()
        element.click()
        time.sleep(4)

    element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop % 10 + 1}]')  # 페이지 번호버튼 클릭
    page = element.text
    element.click()
    print(page, "페이지 시작!!")
    time.sleep(2)

    if loop == looping_num - 1:
        num = num_goods - (looping_num - 1) * 100
    else:
        num = 100

    for i in reversed(range(num)):
        t_name = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i + 1}]/td[5]/div/p/a').text
        t_company = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i + 1}]/td[10]').text
        try:
            t_company = re.search('(.*)\shttp.*', t_company).group(1)
        except:
            t_company = ""

        if (t_name, t_company) in goods_list:

            time.sleep(.5)
            element = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i+1}]/td[1]/input')
            action.move_to_element(element).click().perform()
            time.sleep(.5)
            dup += 1
            print("중복클릭",(t_name, t_company))

        else:
            goods_list.append((t_name, t_company))
            print(i,"중복아님")

    if dup > 0:
        time.sleep(.5)
        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[3]/div[1]/a[6]')
        action.move_to_element(element).click().perform()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])
        print("중복삭제!!")

print(error_list)