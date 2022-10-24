import pandas as pd
import time
import warnings
import back_data_mine
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

print("delivery요청 작성 시작 - delivery form, master_rs 작성")
num_try = 2 #사입요청 몇개? 1개부터

# 기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
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
#사입현황으로 가기
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').click()
time.sleep(1)

d = {}
for i in range(num_try): #https://stackoverflow.com/questions/30635145/create-multiple-dataframes-in-loop
    driver.find_element_by_xpath(f'//*[@id="purchasesList"]/tbody/tr[{i+1}]/td[2]').click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[1])
    df_ps = pd.read_html(driver.page_source, match = '상품 번호')
    df_p = df_ps[1]
    df_p.columns = df_p.columns.get_level_values(1)
    d[i] =df_p
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(.5)

df_pf = pd.concat(d.values(), ignore_index=True)

df_pfs = df_pf[['기타메모1','상품 번호','사입 성공 수량','사입사 메모','사입 입고 예정일']]
list_ = df_pfs.values.tolist()
dict_ = {}
for i in range(len(list_)):
    dict_[list_[i][0]] = [list_[i][1],list_[i][2],list_[i][3],list_[i][4]]
print("사입 딕셔너리 완성")

#master 가져오기
timestr = time.strftime("%Y%m%d")
timestr_y = str(int(timestr)-1)

file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+".xlsx"
df = pd.read_excel (file_name_master, sheet_name=0) # 0에 다 통합해 놓을꺼니까 항상 0
df['수령인 우편번호'] = df['수령인 우편번호'].astype(str)

zip_code = []
for i in range(len(df)):
    if len(df['수령인 우편번호'][i])==4:
        z_code = '0'+df['수령인 우편번호'][i]
    else:
        z_code = df['수령인 우편번호'][i]
    zip_code.append(z_code)
df['수령인 우편번호'] = zip_code
print("마스터 df import 완료")

# 사입결과 df에 입력하기
p_result = [] # 사입번호
p_number = [] # stock 수량
p_info_1 = []
p_info_2 = []
for i in range(len(df)):
    result = '' #번호
    num = 0 #수량
    info1 = '처음값'
    info2 = '처음값'
    if df['상품품목코드'][i] in dict_:
        # 사입사 메모 입력,사입번호 넣기
        info1 = dict_[df['상품품목코드'][i]][2]
        info2 = dict_[df['상품품목코드'][i]][3]
        result = dict_[df['상품품목코드'][i]][0]
        if dict_[df['상품품목코드'][i]][1]>0:
            #stock 개수 넣기
            for j in range(df['구매수량'][i].item()):
                if dict_[df['상품품목코드'][i]][1]>0: #재고개수 >0?
                    num +=1
                    dict_[df['상품품목코드'][i]][1] -= 1
        p_result.append(result)
        p_number.append(num)
        p_info_1.append(info1)
        p_info_2.append(info2)
    else:
        p_result.append("구매목록에 없음")
        p_number.append(0)
        p_info_1.append('구매목록에 없음')
        p_info_2.append('구매목록에 없음')

df['사입번호'] = p_result
df['사입수량'] = p_number
df['배송수량'] = df['사입수량']+df['in_stock']
df['수량check'] = df['수량']==df['배송수량']
df['info_1'] = p_info_1
df['info_2'] = p_info_2

df_deliv = df[['수령인','수령인 전화번호','수령인 우편번호','수령인 주소(전체)','사입번호','배송수량','수량check']]
df_deliv.insert(0,'balnk0','')
df_deliv.insert(1,'blank1','')
df_deliv.insert(2,'temp_배송방법','일반배송')
df_deliv.insert(7,'blank7','')
df_deliv.insert(8,'blank8','')
df_deliv.insert(9,'_sender','Soyool')
df_deliv.insert(10,'_sender_phone','010-8877-5980')
df_deliv.insert(11,'_sender_zip','03121')
df_deliv.insert(12,'_sender_addr','서울 종로구 지봉로 19 3층 딜리버드')
df_deliv.insert(13,'temp13','')
df_deliv.insert(14,'temp14','')
df_deliv.insert(15,'temp15','')
df_deliv.insert(16,'temp16','')
df_deliv.insert(18,'_재고구분','정상')

#사입수량 모자란 부분 제거

df_deliv = df_deliv.loc[df_deliv['수량check'] == True]

#공백 추가
df_deliv.loc[-1]= ""
df_deliv.index = df_deliv.index + 1
df_deliv = df_deliv.sort_index()

file_deliver = "/Users/seoyulejo/Downloads/files/order_deliver_"+timestr_y+".xlsx"
file_purchase = "/Users/seoyulejo/Downloads/files/purchase_"+timestr_y+".xlsx"
file_name_master_rs = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+"_rs.xlsx"

df_deliv.to_excel(file_deliver, index=False)
df_pf.to_excel(file_purchase, index=False)
df.to_excel(file_name_master_rs, index=False)
print("엑셀 export 완료")

"""
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df_deliv)
"""