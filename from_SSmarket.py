
from bs4 import BeautifulSoup # 파싱된 데이터를 python에서 사용하기 좋게 변환
from selenium import webdriver # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os

import time
import requests

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver")
driver.implicitly_wait(20)
url= 'https://sinsangmarket.kr/'
driver.get(url)
driver.maximize_window()
action= ActionChains(driver)

#신상마켓 로그인
driver.find_element_by_class_name("px-6px").click()
time.sleep(1)
action.send_keys('chanelj77').perform()
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[2]/input').click()
action.send_keys('crosscd123!').perform()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button').click()

#찜 목록으로 들어가기
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[3]/a/span').click()

#페이지 아래까지 한번 갔다오
for i in range(10):
    time.sleep(1)
    action.send_keys(Keys.PAGE_DOWN).perform()

action.send_keys(Keys.HOME).perform()
time.sleep(1)

#실행 횟수
number_ = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div/section/article/div/button').text
number = int(number_.split('/')[1].split(')')[0])
print(number)

#루핑시작
for j in range(number): #number재설정 하기
    j += 1
    # 아이템화면 진입

    driver.find_element_by_xpath(
    f'//*[@id="app"]/div[1]/div[2]/div/div/section/div/article/div[{j}]/div[1]/div[1]/img').click()
    time.sleep(2)
    #제목따기
    subject = driver.find_element_by_xpath('// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    r = soup.select_one('.swiper-wrapper')
    s = r.find_all("img")

    count=0
    os.mkdir(f"/Users/seoyulejo/Downloads/{j}_{subject}")
    for i in s:
        link = i.attrs['src']
        time.sleep(1)
        print(link)
        res = requests.get(link)
        if res.status_code == 200:
            with open(f"/Users/seoyulejo/Downloads/{j}_{subject}/{j}{subject}_{count + 1}.jpg", "wb") as file:
                file.write(res.content)
        count+=1


    time.sleep(1)
    #찜목록으로 재진입
    action.send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    #찜해제
    #driver.find_element_by_xpath('// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / div[3] / div[2] / div[2] / button').click()
    #리스트 진입


print("finished")
driver.close()
