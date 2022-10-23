import pandas as pd
from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
import re
import time
import warnings
import back_data_mine
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import zipfile
import glob
import os
from openpyxl import load_workbook

print("송장번호 입력 시작!")

# 기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
search_dir = "/Users/seoyulejo/Downloads/shopping_raw/" # 필요한 경우 편집
prefs = {'download.default_directory' : search_dir}
options.add_experimental_option('prefs', prefs)
#options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
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
"""time.sleep(.5)
try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass"""

# 한글로 바꾸기
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/div').click()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/ul/li[1]/label').click()
time.sleep(.5)

# 광고 있으면 close
"""try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass"""

#딜리버드로 가기
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[1]/div').click()
time.sleep(.5)
print("딜리버드 진입")
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[5]/a').click() #배송현황 클릭
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="returnSearch"]/div[2]/div/label[1]').click() #오늘 클릭
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="orderList_wrapper"]/div[1]/div[2]/div/button').click() #엑셀다운로드 클릭
time.sleep(.5)
print("배송현황 다운로드 완료")

files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name = files[-1]

df_invoice = pd.read_excel(file_name)
print("df_invoice import 완료:",len(df_invoice),"개")

#master 파일 import 하기
timestr = time.strftime("%Y%m%d")
timestr_y = str(int(timestr)-1) #어제날짜

file_name_master_rs = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+"_rs.xlsx"
df = pd.read_excel (file_name_master_rs, sheet_name=0) # 0에 다 통합해 놓을꺼니까 항상 0
print("마스터 df import 완료")

df = df.merge(df, df_invoice[['고객사 주문번호'],['송장번호'],['배송 요청 번호']], left_on="주문번호", right_on="고객사 주문번호", how="left")

# 송장번호 입력
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

select = Select(driver.find_element_by_xpath('//*[@id="QA_prepareNumber2"]/div[5]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

driver.find_element_by_xpath('//*[@id="search_button"]').click() #검색

num_goods = driver.find_element_by_xpath('//*[@id="QA_prepareNumber2"]/div[3]/div[1]/p/strong').text
num_goods = int(num_goods)

for i in range(num_goods):
    order_num = driver.find_element_by_xpath(f'//*[@id="copyarea_{i}"]').text
    product = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/p[1]/a[2]').text
    product =product.split("\n")[0]
    option1 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/ul/li[1]').text
    option1 = option1.split(" : ")[1]
    option2 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/ul/li[2]').text
    option2 = option2.split(" : ")[1]

    new_df = df[(df['주문번호'] == order_num) & (df['상품명(한국어 쇼핑몰)'] == product) & (df['option1'] == option1) & (df['option2'] == option2)]



