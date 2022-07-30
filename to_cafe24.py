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

for i in range(len(all_dirs)): #len(all_dirs)
    #상품간단등록으로 들어가기
    driver.execute_script('window.open("http://crosschungdam.cafe24.com/disp/admin/shop1/product/ProductSimpleRegister");')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)

    #상품제목
    driver.find_element_by_xpath('//*[@id="product_name"]').click()
    time.sleep(1)
    action.send_keys(all_dirs[i].split('_')[-1]).perform()
    time.sleep(.5)

    driver.find_element_by_xpath('//*[@id="product_price"]').click()
    time.sleep(.5)
    action.send_keys(11111).perform()
    time.sleep(.5)

    #상세페이지 이미지 업로드
    #직접작성클릭
    driver.find_element_by_xpath('//*[@id="nnedit"]').click()
    time.sleep(1)
    #다중이미지선택
    driver.find_element_by_xpath('//*[@id="insertFiles-1"]').click()
    time.sleep(1)

    #파일선택
    dir=join(mypath, all_dirs[i]) #폴더지정
    files = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]
    list_file = '\n'.join(files)
    driver.find_element_by_xpath('//*[@id="fr-files-upload-layer-1"]/div/div[2]/input').send_keys(list_file)
    time.sleep(1)
    #전체선택
    driver.find_element_by_xpath('//*[@id="checkAll-1"]').click()
    time.sleep(1)
    #올리기
    driver.find_element_by_xpath('//*[@id="insertAll-1"]').click()
    time.sleep(1)

    #옵션
    action.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)

    #옵션 사용
    driver.find_element_by_xpath('//*[@id="QA_register4"]/div[2]/div/table/tbody/tr/td/div[1]/div/label[1]').click()
    time.sleep(1)

    driver.find_element_by_xpath('// *[ @ id = "eOptionInputCheckbox"]').click()
    time.sleep(1)


    """#옵션설정
    driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[2]/td[3]/input').click()
    time.sleep(1)
    action.send_keys('색상').pause(.1).send_keys(Keys.TAB)\
        .pause(.1).send_keys("블랙").pause(.1).send_keys(Keys.TAB)\
        .pause(.1).send_keys("화이트").pause(.1).send_keys(Keys.TAB)\
        .pause(.1).send_keys(Keys.TAB).pause(.1).perform()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[3]/td[3]/input').click()
    action.send_keys('사이즈').pause(.5).send_keys(Keys.TAB).pause(.5).send_keys("프리").send_keys(Keys.TAB).pause(.5).send_keys(Keys.TAB).pause(.5).perform()
    time.sleep(1)

    #옵션추가
    driver.find_element_by_xpath('//*[@id="eOptionInputPanel"]/div[3]/div/a').click()
    time.sleep(1)"""




print("finished")
time.sleep(30)

















