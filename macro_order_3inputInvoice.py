import pandas as pd
import time
import warnings
import back_data_mine
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import glob
import os
import re
from datetime import datetime, timedelta

print("카페24에 송장번호 입력 시작!")

# 기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
search_dir = "/Users/seoyulejo/Downloads/files/" # 필요한 경우 편집
prefs = {'download.default_directory' : search_dir}
options.add_experimental_option('prefs', prefs)
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
driver.maximize_window()
driver.implicitly_wait(15)
action = ActionChains(driver)
wait = WebDriverWait(driver, 20)

category_list = back_data_mine.category_list # 분류설정


# 신상마켓 로그인
driver.get('https://sinsangmarket.kr/login')
"""try:
    driver.find_element_by_xpath('//*[@id="alert"]/div/div/button').click() #too many segment 버튼 클릭
except:
    pass"""

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

#딜리버드로 가기 (송장번호 get)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[1]/div').click()
time.sleep(.5)
print("딜리버드 진입")

driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[5]/a').send_keys(Keys.ENTER) #배송현황 클릭
time.sleep(4)
try:
    driver.find_element_by_xpath('//*[@id="returnSearch"]/div[2]/div/label[1]').click() #오늘 클릭
    time.sleep(1)
except:
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="returnSearch"]/div[2]/div/label[1]').click()  # 오늘 클릭
    time.sleep(1)
driver.find_element_by_xpath('//*[@id="orderList_wrapper"]/div[1]/div[2]/div/button').send_keys(Keys.ENTER) #엑셀다운로드 클릭
time.sleep(.5)
print("배송현황 다운로드 완료")

files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name = files[-1]

df_invoice = pd.read_excel(file_name, converters={'받는 사람 연락처':str})
df_invoice['key'] = df_invoice['받는 사람 이름'].str.strip() + "_" + df_invoice['받는 사람 연락처'].str.strip()
df_invoice['송장번호'] = df_invoice['송장번호'].fillna(0)
df_invoice['송장번호'] = df_invoice['송장번호'].astype(str)
df_invoice = df_invoice[['key','송장번호']] #연락처에 - 없음
df_invoice = df_invoice.drop_duplicates()
df_invoice = df_invoice.set_index('key')['송장번호']
print("df_invoice import 완료:",len(df_invoice),"개")

#master 파일 import 하기....,
timestr = time.strftime("%Y%m%d")
yesterday = datetime.now() - timedelta(1)
timestr_y = datetime.strftime(yesterday, '%Y%m%d')

file_name_master_rs = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+"_rs.xlsx"
df = pd.read_excel (file_name_master_rs, sheet_name=0) # 0에 다 통합해 놓을꺼니까 항상 0
print("마스터 df import 완료")

df['수령인 전화번호'] = df['수령인 전화번호'].str.replace('-','')
df['수령인'] = df['수령인'].str.strip()
df['key2']= df['수령인']+"_"+df['수령인 전화번호']

df['송장번호']= df['key2'].map(df_invoice) #merge로 할수도 있음.
df.loc[df['수량check'] == False, '송장번호'] = ""
df.loc[df['배송수량'] < 1, '송장번호'] = ""

df['상품명(한국어 쇼핑몰)'] = df['상품명(한국어 쇼핑몰)'].str.replace("티&탑","티-탑")

df['수량check'] = df['수량check'].map({True: 'True', False: 'False'})
df['key3'] = df['주문번호']+"_"+df['상품명(한국어 쇼핑몰)']+"_"+df['상품옵션']+"_"+df['수량check']
df['deliver_check'] = ''
print("마스터 df 송장번호 update") #마켓 상품은 옵션이름이 특별하니까.. 이렇게 처리

## 송장번호 입력
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
driver.find_element_by_xpath('//*[@id="QA_deposit1"]/div[1]/table/tbody/tr[1]/td/a[6]').click() #지난 한달 선택
time.sleep(1)

select = Select(driver.find_element_by_xpath('//*[@id="QA_prepareNumber2"]/div[4]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

driver.find_element_by_xpath('//*[@id="search_button"]').click() #검색

num_goods = driver.find_element_by_xpath('//*[@id="QA_prepareNumber2"]/div[2]/div[1]/div/strong').text
num_goods = int(num_goods)

acc_num =0
we_map_double = []
for i in range(num_goods):
    key = ""
    value = ""
    invoice = ""
    num = 0

    market = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[3]/img').get_property('title')
    element = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[3]')
    val = int(element.get_attribute("rowspan"))
    loop = val -1
    order_num = driver.find_element_by_xpath(f'//*[@id="copyarea_{i}"]').text

    if market == '위메프' and loop >1:
        we_map_double.append(order_num)
        continue

    for j in range(loop):
        if j ==0:
            product = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/p[1]').text
            product = re.search("내역 (.*)\n\(.*",product).group(1)
            product = product.replace("티&탑","티-탑")
            option1 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/ul/li[1]').text
            option1 = option1.replace(" : ","=").strip()
            try:
                option2 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[1]/td[10]/div/ul/li[2]').text
                option2 = option2.replace(" : ","=").strip()
            except:
                option2 = ""
        else:
            product = driver.find_element_by_xpath(
                f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[{j+1}]/td[3]/div/p[1]').text
            product = re.search("내역 (.*)\n\(.*",product).group(1)
            product = product.replace("티&탑", "티-탑")
            option1 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[{j+1}]/td[3]/div/ul/li[1]').text
            option1 = option1.replace(" : ", "=").strip()
            try:
                option2 = driver.find_element_by_xpath(f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[{j+1}]/td[3]/div/ul/li[2]').text
                option2 = option2.replace(" : ", "=").strip()
            except:
                option2 = ""

        option_ =""
        if option2 == "":
            option_ = option1
        else:
            option_ = option1+", "+option2

        key =order_num+"_"+product+"_"+option_+"_True"
        idx = df.index[df['key3'].str.lower() == key.lower()].tolist()
        if len(idx) == 1:
            invoice = df['송장번호'].iloc[idx[0]]
            if invoice == '': # skip으로 수량=0으로 true인 경우.
                print(i, "-", j, "매칭정보 없음")
                continue
            #invoice = int(invoice)
            df['deliver_check'].iloc[idx[0]] = "OK"
            if j==0:
                driver.find_element_by_xpath(
                    f'//*[@id="shipedReadyList"]/table/tbody[{i+1}]/tr[{j+1}]/td[6]/input[1]').click()
            else:
                driver.find_element_by_xpath(
                    f'//*[@id="shipedReadyList"]/table/tbody[{i + 1}]/tr[{j + 1}]/td[1]/input[1]').click()
            num += 1
            acc_num += 1
            print(i,"-",j,"클릭 완료")
        elif len(idx) >1:
            for k in range(len(idx)):
                value = "key3 매칭이 2개이상.. 뭔가 이상"
                df['deliver_check'].iloc[idx[k]]= value
            print(i, "-", j, "key 매칭이 2개이상.. 뭔가 이상")
        else:
            print(i,"-",j,"매칭정보 없음")

    if num > 0: # 인보이스번호 입력
        driver.find_element_by_xpath(f'//*[@id="invoice_no_{i}"]').click()
        action.send_keys(invoice).perform()

df.drop(['key2','key3'], axis=1, inplace=True)

#엑셀 export
file_name_master_rsi = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+"_rsi.xlsx"
df.to_excel(file_name_master_rsi, index=False)
print("df export 완료")

time.sleep(2)
driver.find_element_by_xpath(f'//*[@id="eShipStartBtn"]').send_keys(Keys.ENTER) # 배송중 클릭
time.sleep(4)

alert = driver.switch_to.alert
alert.accept()
time.sleep(2)

try:
    alert = driver.switch_to.alert
    print(alert.text)
    alert.accept()
    print("배송중 처리(건): ", acc_num, "/", len(df[df['배송수량'] > 0]))
except:
    pass

print("위메프 수동처리할 건(복수주문): ", we_map_double)
time.sleep(3)