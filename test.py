
from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import time
import requests
import pyautogui
import warnings
import shutil
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import back_data
from selenium.webdriver.support.ui import Select
import math

fakes = ['디옷','디올','디오르','디욜','샤x','샤널','에르','에르메스','샤','구구','GC','구c','CHA','루이','베네','타이틀','PXG','탐브',
         '프라','MI','몽끌','에트로','베르체']
################################여기 입력해 주기###################################

urls = [('https://sinsangmarket.kr/store/25101?isPublic=1',"스튜디오W 3층 43호 퍼프","yes","no")]
#jjim_order = "yes" #No : 최신순, Yes: 찜
for_man = "no" #남자옷이면 "yes"

start = [0,0] # 상품 중간시작시 (0부터 시작) (ex 3까지 완료됬으면 3으로 넣으면 됨)
number_d = 100 # 0일 경우 모든 상품, 지정하려면 숫자 입력

margin = .2
delivery_fee = 4000 #from 구매처:3000, to 고객:1000 (고객 부담 3000 -2000)
down_path = '/Users/seoyulejo/Downloads/imgs/'
###############################################################################


warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver") #, options=options
driver.maximize_window()
driver.implicitly_wait(15)
driver.get('https://sinsangmarket.kr/login')
action = ActionChains(driver)
wait = WebDriverWait(driver, 10)

# 신상마켓 로그인
try:
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div/div[2]/div[3]/p').click()
except:
    pass
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[1]/input').click()
action.send_keys('chanelj77').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[2]/input').click()
action.send_keys('crosscd123!').perform()
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
action.send_keys('crosschungdam').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('crosscd123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(.5)
driver.get("https://crosschungdam.cafe24.com/admin/php/main.php") # new 관리자 화면 진입
print("cafe24 진입")
time.sleep(.7)

######################## 샵별 추가 코드 ###################3

# 상품목록 진입
driver.get('https://crosschungdam.cafe24.com/disp/admin/shop1/product/productmanage')
time.sleep(1)
select = Select(driver.find_element_by_xpath('//*[@id="eSearchFormGeneral"]/li/select[1]')) #검색종류
select.select_by_visible_text('공급사 상품명')
time.sleep(.3)
driver.find_element_by_xpath('//*[@id="eSearchFormGeneral"]/li/input').click() #검색창클릭
time.sleep(.3)
action.send_keys(urls[0][1]).perform()
time.sleep(.3)
driver.find_element_by_xpath('//*[@id="eBtnSearch"]').click() # 조회버튼 클릭
time.sleep(1)

#상품 목록 출력
num_goods = driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[1]/p').text
num_goods = int(num_goods.split(" ")[1].split("개")[0])
print(f"총상품개수: {num_goods}개")

looping_num = num_goods/100
looping_num = math.ceil(looping_num)

#100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]')) #검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

#목록 뽑기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
goods_list_s = soup.find_all("a", attrs={"class":"txtLink eProductDetail ec-product-list-productname"})
goods_list = []
for good in goods_list_s:
    goods_list.append(good.get_text())
time.sleep(.5)

if looping_num > 1:
    for loop in range(looping_num-1):
        driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop+2}]/a').click()  # 조회버튼 클릭
        time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        goods_list_s = soup.find_all("a", attrs={"class": "txtLink eProductDetail ec-product-list-productname"})
        for good in goods_list_s:
            goods_list.append(good.get_text())

print(goods_list)

################# 신상마켓 샵별 상품 정보 따기
driver.switch_to.window(driver.window_handles[0])
url = urls[0][0]
# seller id 추출
p = re.compile(r'sinsangmarket.kr/store/([0-9]+)')
m = p.search(url)
id = m.group(1)
time.sleep(2)

# seller 샵으로 들어가기
time.sleep(.5)
driver.get(url)
time.sleep(.5)
print("셀러샵 진입: " , id)
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html , 'html.parser')
if soup.find("div" , string=' 매장 TOP 30 '):
    location = 3
else:
    location = 2

# 찜순 선택순
if urls[0][2].lower() == "yes":
    url = url.split("?")
    url = url[ 0 ] + "?sort=likes&" + url[ 1 ]
    driver.get(url)
    print("찜순 선택")
    time.sleep(1)
else:
    print("최신순 선택")

# 수행 횟수 구하기
number_ = driver.find_element_by_xpath(f'//*[@id="{id}"]/div/div[{location}]/div/div[1]/div[1]').text
number_ = int(number_.split(" ")[ 1 ].split("개")[ 0 ].replace("," , ""))
if number_d == 0:
    number = number_
elif number_d >= number_:
    number = number_
else:
    number = number_d

print("상품 개수: " , number_)
print("루핑 횟수: " , number)

# 페이지 아래까지 한번 갔다오기
for i in range(round(number / 6)):
    action.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(.2)
action.send_keys(Keys.HOME).perform()
print("스크롤 완료")
#--------------------
#목록따기 - 신상
html = driver.page_source
soup = BeautifulSoup(html , 'html.parser')

goods_title = []
goods_title_s = soup.find_all("p", attrs={"class":"post-content__title"})
for good in goods_title_s:
    goods_title.append(good.get_text().strip())
time.sleep(.5)



# ------------------여기까지 기본 세팅
