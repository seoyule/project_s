# 테스트

from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import time
import requests
import pyautogui


driver = webdriver.Chrome("/Users/seoyulejo/chromedriver")
driver.implicitly_wait(10)
url = 'https://eclogin.cafe24.com/Shop/'
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

# cafe24 열기
driver.find_element_by_xpath('//*[@id="mall_id"]').click()
time.sleep(.5)
action.send_keys('crosschungdam').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('crosscd123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(4)

#마켓플레이스 진입
driver.get("https://mp.cafe24.com/mp/main/front/service")
time.sleep(.5)
driver.get("https://mp.cafe24.com/mp/product/front/manageList")
time.sleep(1)
#전송실패 진입
driver.find_element_by_xpath('//*[@id="stats_send_fail_count"]/span').click()
time.sleep(1)
#첫번째 아이템 클릭 -  새창뜸
driver.find_element_by_xpath('//*[@id="eMultiTable"]/tbody/tr[1]/td[16]/button').click()
time.sleep(.5)
driver.switch_to.window(driver.window_handles[1])
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="footer"]/a[3]').click() # 수정 버튼
time.sleep(2)
action.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="QA_register_product"]/div[2]/table/tbody/tr[13]/td[2]/div[2]/div/label[1]').click()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="footer"]/a[6]').click()
time.sleep(4)
alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[0])





