from bs4 import BeautifulSoup # 파싱된 데이터를 python에서 사용하기 좋게 변환
from selenium import webdriver # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os


import time
import requests

from os import listdir
from os.path import isfile,isdir, join


driver = webdriver.Chrome("/Users/seoyulejo/chromedriver")
driver.implicitly_wait(20)
url= 'https://eclogin.cafe24.com/Shop/'
driver.get(url)
driver.maximize_window()
action= ActionChains(driver)

#폴더정보 생성
#mypath = "/Users/seoyulejo/Pictures/상품/6:10(todo)"
mypath = "/Users/seoyulejo/Downloads"
all_dirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]

#cafe24 로그인
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="mall_id"]').click()
time.sleep(.5)
action.send_keys('crosschungdam').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('crosscd123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(3)

    #상품간단등록으로 들어가기
driver.execute_script('window.open("http://crosschungdam.cafe24.com/disp/admin/shop1/product/productregister");')
time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
time.sleep(5)

action.send_keys(Keys.PAGE_DOWN).pause(.5).send_keys(Keys.PAGE_DOWN).pause(.5).send_keys(Keys.PAGE_DOWN).pause(.5).send_keys(Keys.PAGE_DOWN).perform()
time.sleep(5)

#상품등록

driver.find_element_by_xpath('//*[@id="imgRegisterContainer"]/ul/li[1]/span[4]').send_keys(r'/Users/seoyulejo/Downloads/1_bl6049 3cm 소가죽/1bl6049 3cm 소가죽_1.jpg')

time.sleep(10)




















