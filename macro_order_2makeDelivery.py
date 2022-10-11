import pandas as pd
import time
import warnings
import back_data_mine
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

print("delivery요청 작성 시작")
num_try = 2

############################
#사입결과 가져오기

# 기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")

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
#사입현환으로 가기
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').click()
time.sleep(1)

'//*[@id="purchasesList"]/tbody/tr[1]/td[1]'
'//*[@id="purchasesList"]/tbody/tr[2]/td[1]'
'//*[@id="purchasesList"]/tbody/tr[1]/td[2]'

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

df_pfs = df_pf[['기타메모1','상품 번호','사입 성공 수량']]
list_ = df_pfs.values.tolist()
dict_ = {}
for i in range(len(list_)):
    dict_[list_[i][0]] = [list_[i][1],list_[i][2]]
print("사입 딕셔너리 완성")

#master 가져오기
timestr = time.strftime("%Y%m%d")
timestr_y = str(int(timestr)-1)

file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+".xlsx"
df = pd.read_excel (file_name_master, sheet_name=0) # 0에 다 통합해 놓을꺼니까 항상 0

p_result = []
for i in range(len(df)):
    num = 0
    for j in range(len(df['구매수량'][i])):
        if df['상품품목코드'][i] in dict_:
            if dict_[df['상품품목코드'][i]][1]>0: #사입 재고개수 >0?
                num +=1
                dict_[df['상품품목코드'][i]][1] -= 1
        else:
            print("상품품목코드 없음",df['상품품목코드'][i])
    p_result.append(num)
df['사입결과'] = p_result

file_name_master_wr = "/Users/seoyulejo/Downloads/files/order_master_"+timestr_y+"_wr.xlsx"
df.to_excel(file_name_master_wr)
print("엑셀 export 완료")
