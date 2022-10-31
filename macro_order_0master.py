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

#추가작업? - 몇개 추가? 0 은 모두..
add = 0
print("추가작업:",add,"개")

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
    driver.find_element_by_xpath('//*[@id="alert"]/div/div/button').click() #too many segment 버튼 클릭
except:
    pass

try:
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/header/div/div[2]/div[3]/p').click() #start 버튼 클릭
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

#엑셀 다운로드
driver.find_element_by_xpath('//*[@id="eExcelDownloadBtn"]').click()
time.sleep(1)
driver.switch_to.window(driver.window_handles[2])

select = Select(driver.find_element_by_xpath('//*[@id="aManagesList"]'))
select.select_by_visible_text('ForOrderSejo')
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="Password"]').click()
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="PasswordConfirm"]').click()
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="QA_common_password1"]/div[3]/a').click() #자료 요청
time.sleep(.5)

alert = driver.switch_to.alert
alert.accept()
driver.switch_to.window(driver.window_handles[2])

time.sleep(10)
driver.find_element_by_xpath('//*[@id="QA_common_password2"]/div[3]/table/tbody/tr[1]/td[7]').click() #다운로드 버튼

driver.find_element_by_xpath('//*[@id="password"]').click() #다시 비밀번호 물어봄
action.send_keys('protest123').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="reason_for_download"]').click() #이유 적어줌
action.send_keys('analysis').perform()
time.sleep(.5)

driver.find_element_by_xpath('//*[@id="excel_download"]').click() #파일요청
time.sleep(7)
driver.close()
driver.switch_to.window(driver.window_handles[1])

print("다운로드 완료")
#다운로드 zip 파일 이름 확인 https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_path = files[-1]

#zip 풀기
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall(search_dir, pwd=b'protest123')
print("압축해제 완료")

#변환 파일 이름 확인 https://stackoverflow.com/questions/168409/how-do-you-get-a-directory-listing-sorted-by-creation-date-in-python
files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name = files[-1]

df = pd.read_csv(file_name)
if add !=0:
    df = df.drop(df.index[0:add*-1])
    df = df.reset_index(drop=True)
print("df import 완료:",len(df),"개")

df['option1'] = df['상품옵션'].replace('.*=(\S+),.*',r'\1', regex=True)
df['option2'] = df['상품옵션'].replace('.*=.*=(.*)',r'\1', regex=True)
df['option2'] = df['option2'].str.lower()
df['수령인 우편번호'] = df['수령인 우편번호'].astype(str)

zip_code = []
for i in range(len(df)):
    if len(df['수령인 우편번호'][i])==4:
        z_code = '0'+df['수령인 우편번호'][i]
    else:
        z_code = df['수령인 우편번호'][i]
    zip_code.append(z_code)
df['수령인 우편번호'] = zip_code

title_ss = []
price_ss = []
shop_name = []
building_name = []
shop_location = []
shop_phone_number = []
note = []

print("데이터 채우기 시작")
for i in range(len(df)):
    link = df['모델명'][i]
    driver.switch_to.new_window('tab')
    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[2])
    #url 검
    try:
        driver.get(link)
        time.sleep(1.5)
    except:
        note.append('!! url 없음 !!')
        title_ss.append('!! url 없음 !!')
        price_ss.append('!! url 없음 !!')
        shop_name.append('!! url 없음 !!')
        building_name.append('!! url 없음 !!')
        shop_location.append('!! url 없음 !!')
        shop_phone_number.append('!! url 없음 !!')

        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(.5)
        print(i+1,"url 없음 skip")
        continue

    # 도매상품이름
    try:
        title = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/p').text
        title_ss.append(title)
    except:
        note.append('!! link 이상 !!')
        title_ss.append('!! link 이상 !!')
        price_ss.append('!! link 이상 !!')
        shop_name.append('!! link 이상 !!')
        building_name.append('!! link 이상 !!')
        shop_location.append('!! link 이상 !!')
        shop_phone_number.append('!! link 이상 !!')

        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(.5)
        print(i + 1, "link 이상 skip")
        continue

    #품절확인
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div", attrs={'class': 'sold-out'}):
        note.append('!! sold-out !!')
    else:
        note.append('OK')

    time.sleep(.5)
    #도매가격
    price = int(driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/span').text.replace(",",""))
    price_ss.append(price)
    time.sleep(.5)

    #가게 화면 진입
    driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').click()
    time.sleep(1.5)
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(.5)
    #가게이름
    shop_n = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/span').text
    shop_name.append(shop_n)
    time.sleep(.5)
    #전화번호
    shop_p = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div').text.strip()
    shop_phone_number.append(shop_p)
    time.sleep(.5)

    address = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div').text.strip()
    #빌딩이름
    try:
        building_n = re.search(r'(.*)\s\S+층\s.*', address).group(1)
    except:
        try:
            building_n = re.search(r'(.*\s별관)\s.*', address).group(1)
        except:
            building_n = address
    building_name.append(building_n)
    time.sleep(.5)
    #주소
    try:
        shop_l = re.search(r'.*\s(\S+층\s.*)', address).group(1)
    except:
        try:
            shop_l = re.search(r'.*\s별관\s(.*)', address).group(1)
        except:
            shop_l = address
    shop_location.append(shop_l)
    time.sleep(.5)

    driver.close()
    driver.switch_to.window(driver.window_handles[2])
    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    print(i+1,"완료")

df['title_ss'] = title_ss
df['price_ss'] = price_ss
df['shop_name'] = shop_name
df['building_name'] = building_name
df['shop_location'] = shop_location
df['shop_phone_number'] = shop_phone_number
df['note'] = note

cols = df.columns.tolist()
cols = cols[:11]+cols[12:14]+cols[15:18]+cols[11:12]+cols[14:15]+cols[18:]
df = df[cols]

df.insert(12,'key','')
df.insert(15,'in_stock','')
df.insert(16,'구매수량','')

#재고와 비교위한 key값 생성
df['key'] = df['title_ss']+"_"+df['option1']+"_"+df['option2']

print("데이터 채우기 완료")

####################
#딜리버드에서 재고 다운받기
driver.switch_to.window(driver.window_handles[0])
#딜리버드로 가기
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[1]/div').click()
time.sleep(.5)

print("딜리버드 진입")
#재고로 가기
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/a').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div/div/div/div[3]/div/div/div[2]/label').click()
time.sleep(3)

df_stocks = pd.read_html(driver.page_source, match = '상품번호')
df_stock = df_stocks[1]
df_stock.columns = df_stock.columns.get_level_values(1)
df_stock['도매 매장명'] = df_stock['도매 매장명'].replace('도매\s매장\s변경','',regex=True)
df_stock['상품번호'] = df_stock['상품번호'].replace('상품정보\s수정','',regex=True)
df_stock['key'] = df_stock['도매 상품명']+"_"+df_stock['상품옵션 1']+"_"+df_stock['상품옵션 2']
df_stock['key'] = df_stock['key'].str.lower()

df_stock_ = df_stock[['key','상품번호','정상재고']]
list_ = df_stock_.values.tolist()
dict_ = {}
for i in range(len(list_)):
    dict_[list_[i][0]] = [list_[i][1],list_[i][2]]
print("재고 dic 완료")

p_result = [] # 사입번호
p_number = [] # stock 수량
for i in range(len(df)):
    result = '' #번호
    num = 0 #수량
    if df['key'][i].lower() in dict_:
        # 사입번호 넣기
        result = dict_[df['key'][i].lower()][0]
        if dict_[df['key'][i].lower()][1]>0:
            #stock 개수 넣기
            for j in range(df['수량'][i].item()):
                if dict_[df['key'][i].lower()][1]>0: #재고개수 >0?
                    num +=1
                    dict_[df['key'][i].lower()][1] -= 1
    p_result.append(result)
    p_number.append(num)

#마스터 양식에 재고 반영
df['temp_사입번호'] = p_result
df['in_stock'] = p_number

###############################################3
#dict_ export 해서 두번째 부터 사용하게 코드 여기 삽입
###############################################3

"""df_stock_ = df_stock.groupby(['key'],dropna=False, as_index=False)[['정상재고']].sum()
stocks_ = df_stock_.values.tolist() # stock을 한개씩 리스트로 만들어서 한개씩 빼먹기
stocks = []
for i in range(len(stocks_)):
    for j in range(stocks_[i][1]):
        stocks.append(stocks_[i][0].lower())
print("재고 list 완료")

in_stock = []
temp_code = []
for i in range(len(df)):
    num = 0
    for j in range(df['수량'][i]):
        if df['key'][i].lower() in stocks:
            num += 1
            stocks.remove(df['key'][i].lower())
        else:
            pass
    in_stock.append(num)
df['in_stock'] = in_stock"""

df['구매수량'] = df['수량']-df['in_stock']
print("df에 재고수량 반영")

timestr_now = time.strftime("%Y%m%d-%H%M%S")
timestr = time.strftime("%Y%m%d")

file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr+".xlsx"
file_name_stock = "/Users/seoyulejo/Downloads/files/stock_"+timestr+".xlsx"

if add == 0:
    df.to_excel(file_name_master)
    print("엑셀 export 완료")
else:
    ExcelWorkbook = load_workbook(file_name_master)
    writer = pd.ExcelWriter(file_name_master, engine='openpyxl')
    writer.book = ExcelWorkbook
    df.to_excel(writer, sheet_name=timestr_now)
    writer.save()
    writer.close()

df_stock.to_excel(file_name_stock)

try:
    os.remove(file_path)
    os.remove(file_name)
except OSError as e:
    print(e.strerror)


