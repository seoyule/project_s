# for 변수: k,j,i

import time
import warnings
import math
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


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
wait = WebDriverWait(driver, 15)

# 기본-cafe24: 열기
driver.get("https://eclogin.cafe24.com/Shop/")

time.sleep(.5)
driver.find_element_by_xpath('//*[@id="mall_id"]').click()
time.sleep(.5)
action.send_keys('soyool').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('!QAZwsx123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(1)
# 기본-cafe24: 광고 있으면 close
try:
    driver.find_element_by_class_name("btnClose.eClose").click()
    time.sleep(.3)
except:
    pass
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btnPromodeView')))
#driver.find_element_by_class_name('btnPromodeView').click()# new 관리자 화면 진입 'newPromodeArea
#time.sleep(.5)
print("cafe24 진입")


# 마켓플레이스: 열기
driver.get("https://mp.cafe24.com/mp/main/front/service")
print("마켓플레이스 진입")
driver.get("https://mp.cafe24.com/mp/product/front/manageList")
print("마켓플레이스 상품관리 진입")
time.sleep(0.5)
driver.find_element_by_xpath('//*[@id="stats_status_wait_count"]').click()
time.sleep(0.5)

select = Select(driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩 보기')
time.sleep(1)

num = driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[1]/div[1]/span/strong').text
num = int(num.replace(",",""))
looping_num = math.ceil(num/100)
print(f'총 {looping_num}개 페이지')

for i in range(looping_num):
    print(f'page{i + 1} 시작')
    driver.find_element_by_xpath('//*[@id="product_list"]/div/div[1]/table/thead/tr/th[1]/div/label/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="mk-container"]/div[2]/div[4]/div[2]/div/div[1]/div[1]/div/div/button[1]').click()

    alert = driver.switch_to.alert
    alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(60)

    #wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    print(f'page{i+1} 완료')

print(f'모두 완료')
