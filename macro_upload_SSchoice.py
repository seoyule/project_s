# for 변수: k,j,i
from bs4 import BeautifulSoup  # 파싱된 데이터를 python에서 사용하기 좋게 변환
import os
import re
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import pyautogui
import warnings
import shutil
import math
import back_data_mine
import pickle
from PIL import Image
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


# 기본세팅
start = 1 # 중간부터 시작 시작 - 개수 번째
number = 500 # 아이템 검색 개수
down_path = '/Users/seoyulejo/Downloads/imgs/'
error = []
n = 0 #완료된 상품 개수
subject_list = [] # 중복상품 체크
subject_4f = ""
existing = 0

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

category_list = back_data_mine.category_list # 분류설정
with open('listfile', 'rb') as fp: # url 리스트 불러오기
    urls = pickle.load(fp)

# 기본-신상: 신상마켓 로그인
driver.get('https://sinsangmarket.kr/login')
"""try:
    driver.find_element_by_xpath('//*[@id="alert"]/div/div/button').click() #too many segment 버튼 클릭
except:
    pass
"""
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

# 기본-신상: 광고 있으면 close
time.sleep(.5)
try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass

# 기본-신상: 한글로 바꾸기
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/div').click()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/ul/li[1]/label').click()
time.sleep(.5)

# 기본-신상: 광고 있으면 close
try:
    driver.find_element_by_class_name("button.close-button").click()
    time.sleep(.3)
except:
    pass

# 기본-신상: 신상초이스 진입
driver.get('https://sinsangmarket.kr/sinsangChoice')

# 기본-cafe24: 열기
driver.execute_script('window.open("https://eclogin.cafe24.com/Shop/");')
driver.switch_to.window(driver.window_handles[1])
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

# 기본-cafe24: 상품목록 진입
driver.get('https://soyool.cafe24.com/disp/admin/shop1/product/productmanage')
time.sleep(1)
driver.find_element_by_xpath('//*[@id="eBtnSearch"]').click()  # 조회버튼 클릭
time.sleep(1)

# 기본-cafe24: 상품 목록 출력
num_goods = driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[1]/p').text
num_goods = int(num_goods.split(" ")[1].split("개")[0])
looping_num = num_goods / 100
looping_num = math.ceil(looping_num)
print("총",num_goods,"개")
print("페이지",looping_num,"개")

# 기본-cafe24: 100개씩 보이게
select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]'))  # 검색종류
select.select_by_visible_text('100개씩보기')
time.sleep(1)

for i in range(12):
    action.send_keys(Keys.DOWN).perform()

# 기본-cafe24: 공급사 보이게
driver.find_element_by_xpath('//*[@id="QA_list2"]/div[3]/div[3]/div/a/span').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="listSubject"]/div[1]/ul/li[15]/label').click()
time.sleep(.2)
driver.find_element_by_xpath('//*[@id="eColumnApply"]/span').click()
time.sleep(1)

# 기본-cafe24: 목록 뽑기 (goods_list)
goods_list = []
for loop in range(looping_num): #looping_num
    if loop%10 == 0 and loop !=0: #next page 버튼 누르기
        if loop == 10:
            element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a')
        else:
            element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a[2]')
        action.move_to_element(element).perform()
        element.click()
        time.sleep(4)

    element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop%10 + 1}]') # 페이지 번호버튼 클릭
    page = element.text
    element.click()
    print(page,"페이지 시작!!")
    time.sleep(2)

    if loop == looping_num-1:
        num = num_goods - (looping_num-1)*100
    else:
        num = 100

    for i in range(num):
        t_name = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i+1}]/td[5]/div/p/a').text
        t_company = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i+1}]/td[10]').text
        try:
            t_company = re.search('(.*)\shttp.*', t_company).group(1)
        except:
            t_company = ""
        goods_list.append((t_name, t_company))
    pyautogui.press('ctrl')

print(f"cafe24-거래선 전체상품 list 완료: {len(goods_list)}개")
driver.switch_to.window(driver.window_handles[0])

################## 아이템별 스크린 시작 ####################

if start > 4:
    for i in range(round(start / 8)):
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(.3)
    print("스크롤 완료")
    time.sleep(5)

for j in range(start-1,number):  # 설정하기
    if existing > 200:
        print("cafe24 - 이전 업데이트 포인트 도달")
        break

    try:
        j += 1
        print(j, "번째아이템 시작")

        # 신상: 아이템 클릭 (첫번째 창)
        pyautogui.press('ctrl')  # sleep 방지
        time.sleep(1)
        element = driver.find_element_by_xpath(f'//*[@id="app"]/div[1]/div[2]/div/div[5]/div/div/div[1]/div[{j}]/div[1]')
        action.move_to_element(element).perform()
        element.click()
        time.sleep(.5)
        driver.find_element_by_xpath('//*[@id="goods-detail-modal"]/div/div/div[1]/div/div[2]/div[2]/div[1]/button').click() # 거래선으로 가기.. 없는 경우도 있다.
        time.sleep(1)
        addr = driver.current_url

        # 신상: 아이템화면 진입 (새창- 3번째 창)
        driver.switch_to.new_window('tab')
        time.sleep(.5)
        driver.switch_to.window(driver.window_handles[2])
        driver.get(addr)
        time.sleep(2)

        # 신상: 소스 수집 (새창- 3번째 창)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 신상: 제목따기 (새창- 3번째 창)
        subject_ = driver.find_element_by_xpath('// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text.strip()
        subject_4f = subject_.replace("/", "-")
        subject = back_data_mine.name_change(subject_) #ops등 제목 수정

        # 신상: 거래처따기 (새창- 3번째 창)
        seller = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').text.strip()
        print("거래처: ", seller)
        block_seller = ""
        for i in back_data_mine.block_seller:
            if i in seller:
                block_seller = True
                break
        if block_seller == True:
            print("block seller skip: ", subject)
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상: 기본정보 따기 (새창- 3번째 창)
        table = {}
        datas = soup.find_all("div", attrs={'class': 'w-full flex gap-x-[1px]'})
        #기본 속성
        for data in datas:
            t_key = data.find("div", attrs={
                'class': 'w-[120px] py-[20px] pl-[12px] text-gray-80 flex items-center bg-gray-10'})
            if t_key:
                t_key = t_key.get_text().strip()
            else:
                continue
            t_value = data.find("div", attrs={
                'class': 'information-row__content flex items-center text-gray-100 py-[20px] px-[24px] bg-white-100'})
            if t_value:
                if len(t_value) > 1:
                    t_val = []
                    for i in t_value:
                        t_val.append(i.get_text().strip())
                else:
                    t_val = t_value.get_text().strip()
                table[t_key] = t_val
        #두께 등..
        for data in datas:
            t_key = data.find("div", attrs={
                'class': 'w-[120px] min-w-[82px] flex items-center py-[20px] pl-[12px] text-gray-80 bg-gray-10'})
            if t_key:
                t_key = t_key.get_text().strip()
            else:
                continue
            t_value = data.find("div", attrs={
                'class': 'min-w-[42px] text-gray-100'})
            if t_value:
                t_val = t_value.get_text().strip()
                table[t_key] = t_val
            else:
                continue

        color = table['색상']
        table['색상'] = table['색상'].replace(" ", "").split(',')
        size = table['사이즈']
        table['사이즈'] = table['사이즈'].lower().replace("sml","S,M,L")
        table['사이즈'] = table['사이즈'].replace(" ", "").split(',')
        if table['사이즈'][0] == 'F':
            table['사이즈'][0] = 'Free'
        registered = table['상품등록정보']
        category = table['카테고리'][1]
        category2 = back_data_mine.category_convert[category]
        if table['카테고리'][1] == '티&탑': #상품이름 입력시.. 변환 위함.. (오픈마켓에 &안들어감)
            category_ = '티-탑'
        else:
            category_ = table['카테고리'][1]

        color_ = table['색상']
        size_ = table['사이즈']
        subject = category_ + " " + subject
        print("품명: ", subject)
        print("table: ", table)

        # 신상: 기존 cafe24업로드 여부 확인 (새창- 3번째 창)
        if (subject, seller) in goods_list:
            existing += 1
            print("cafe24에 이미있음 skip: ", subject)
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상: 기존 반품 확인 (새창- 3번째 창)
        block_subject = False
        for f in back_data_mine.block_subject:
            if f in subject:
                block_subject = True
                break

        if block_subject:
            print("기존반품 상품: ", subject)
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상: 중복업데이트확인 (새창- 3번째 창)
        if (subject, seller) in subject_list:
            print("중복상품 업로드 skip")
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상: 품절 확인
        if soup.find("div", attrs={'class': 'sold-out'}):
            print("품절상품 skip")
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform() # 찜목록으로 재진입
            continue

        # 신상: 검색어
        subject_keywords = subject.replace(", ", ",")
        subject_keywords = subject_keywords.replace(" ", ",")
        subject_keywords = subject_keywords.replace("(", ",")
        subject_keywords = subject_keywords.replace(")", ",")
        subject_keywords = subject_keywords.split(",")
        subject_keywords = [subject_keyword[0:18] for subject_keyword in subject_keywords]
        subject_keywords = ",".join(subject_keywords)

        # 신상: 제품 상세설명 따기
        r = soup.find("div", attrs={"class": "row__content"}).get_text()
        if "모델정보" in r:
            try:
                p = re.compile('실측사이즈:.*모델정보[^\n]*', re.DOTALL)
                m = p.search(r)
                comment = m.group()
                comment = comment.lower().replace("\n", "<br>")
                if "모델정보" not in comment:
                    comment = ""
            except:
                r= ""
                comment = ""
        else:
            print("comment에 상세수치 없음")
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상: 이미지 사용가능 여부 체크
        image_avail = ""
        for i in back_data_mine.image_check:
            if i in r:
                image_avail = True
                break
        if image_avail == True:
            print("이미지 사용불가 skip")
            driver.close()  # 창닫기
            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
            continue

        # 신상:가격따기
        price = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/span').text
        price = int(re.sub(r'[^0-9]', '', price))
        price_ = int(round((price * (1.133) + (300 + 1000)) / (1 - (.13 + .3)), -3))
        if price_%10000 ==0:
            price_ -= 1000
        # https://docs.google.com/spreadsheets/d/1ZNMG8hey03UuLasNO5dEvQo1ncBi-GZXVQn6WP5EMZQ/edit#gid=289254889
        print("매입가/판매가: ", price, price_)

        # 이미지 다운로드
        r = soup.select_one('.swiper-wrapper')
        s = r.find_all("img")
        count = 0
        os.mkdir(down_path + f"{j}_{subject_4f}")
        for i in s:
            link = i.attrs['src']
            # print(link)
            res = requests.get(link)
            if res.status_code == 200 and count < 20:
                file_ = down_path + f"{j}_{subject_4f}/{subject_4f}_{count + 1}.jpg"
                file_rs = down_path + f"{j}_{subject_4f}/{subject_4f}_{count + 1}_rs.jpg"
                with open(file_, "wb") as file:
                    file.write(res.content)

                if os.path.getsize(file_) > 2000000:
                    img = Image.open(file_)
                    img = img.convert('RGB')
                    img.save(file_, 'JPEG', qualty=85)

                img = Image.open(file_)  # 이미지 불러오기
                img_size = img.size  # 이미지의 크기 측정
                x = img_size[0]  # 넓이값
                y = img_size[1]  # 높이값
                if x != y:
                    size = max(x, y)
                    resized_img = Image.new(mode='RGB', size=(size, size), color="white")
                    offset = (round((abs(x - size)) / 2), round((abs(y - size)) / 2))
                    resized_img.paste(img, offset)
                    resized_img.save(file_rs)
            count += 1
        print("이미지저장 완료")

        # 세번째 창 닫기
        driver.close() #창닫기

############################# 입력 시작 ###################################3

        # cafe24 상품등록으로 가기 (일반등록)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(.5)
        driver.get("http://soyool.cafe24.com/disp/admin/shop1/product/productregister") # new 관리자 - 등록
        time.sleep(1)

        # 진열상태, 판매상태 업데이트
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[1]/td/label[1]/input')))
        driver.find_element_by_xpath('//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[1]/td/label[1]/input').click()
        driver.find_element_by_xpath('//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[2]/td/label[1]/input').click()
        time.sleep(.3)

        # 상품분류
        try:
            for i in range(len(category_list[category])):
                driver.find_element_by_xpath(category_list[category][i]).click()
                time.sleep(.3)
        except:
            driver.find_element_by_xpath(
                '//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[18]').click()
        driver.find_element_by_xpath('//*[@id="eCategoryTbody"]/tr/td[5]/div').click() #등록

        # 상품명 입력
        time.sleep(.3)
        driver.find_element_by_xpath('//*[@id="product_name"]').click()
        action.send_keys(subject).perform()
        time.sleep(.2)
        driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[2]/td/div[1]/input').click()
        action.send_keys(subject_).perform() #원래 상품명: 영문상품명에 입력
        time.sleep(.2)

        # 등록일 입력 - 상품명(관리용)에..
        driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[3]/td/input').click()
        action.send_keys(table.get('상품등록정보')).perform()
        time.sleep(.3)

        # seller - url 공급사 상품명에 등록
        driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[4]/td/input').click()
        action.send_keys(seller," ",addr).perform()
        time.sleep(.3)

        #url 모델명에 등록
        driver.find_element_by_xpath('//*[@id="eProductModelName"]').click()
        action.send_keys(addr).perform()
        time.sleep(.3)

        #seller 자체 상품코드에 등록
        driver.find_element_by_xpath('//*[@id="ma_product_code"]').click()
        action.send_keys(seller[:39]).perform()
        time.sleep(.5)

        # 상세설명 입력
        html_template_ = "<h2>기본정보</h2><table><tbody>"
        for i in table.keys():
            if i == '낱장 여부':
                continue
            html_template_ = html_template_ +f"<tr><td>{i}</td><td>{table[i]}</td></tr>"
        html_template_ = html_template_ + f"</table></tbody><br><p>{comment}</p><br><p>더 다양한 상품을 soyool샵에서 만나보세요 :) </p><p>https://soyool.co.kr/</p><br>"

        driver.find_element_by_xpath('//*[@id="eTabNnedit"]').click()
        driver.find_element_by_xpath('//*[@id="html-1"]').click()
        action.send_keys(html_template_).perform()
        driver.find_element_by_xpath('//*[@id="html-1"]').click()
        driver.find_element_by_xpath('//*[@id="tabCont1_2"]/div/div/div[2]').click()
        for i in range(30):
            action.send_keys(Keys.ARROW_DOWN).perform()
        driver.find_element_by_xpath('//*[@id="insertFiles-1"]').click() # 다중이미지 클릭
        files = [] #파일선택
        for i in range(len(s)):
            if i<20:
                files.append(down_path+f"{j}_{subject_4f}/{subject_4f}_{i + 1}.jpg")
        list_file = '\n'.join(files)
        time.sleep(.5)
        driver.find_element_by_xpath('//*[@id="fr-files-upload-layer-1"]/div/div[2]/input').send_keys(list_file)
        time.sleep(.5)
        driver.find_element_by_xpath('//*[@id="checkAll-1"]').click() #전체선택
        time.sleep(.5)
        driver.find_element_by_xpath('//*[@id="insertAll-1"]').click() #올리기
        time.sleep(.5)

        #검색어 입력
        element = driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[2]/tbody/tr/td/div/input')
        action.move_to_element(element).perform()
        element.click()
        action.send_keys(subject_keywords[:49]).perform()

        # 가격입력
        element = driver.find_element_by_xpath('//*[@id="product_price"]')
        action.move_to_element(element).perform()
        element.click()
        action.send_keys(price_).perform()
        time.sleep(.5)

        # 옵션설정
        wait.until(EC.element_to_be_clickable((By.XPATH,'// *[ @ id = "eOptionUseT"]')))
        driver.find_element_by_xpath('// *[ @ id = "eOptionUseT"]').click()
        time.sleep(.5)
        wait.until(EC.element_to_be_clickable((By.XPATH,'// *[ @ id = "eUseOptionSetF"]')))
        driver.find_element_by_xpath('// *[ @ id = "eUseOptionSetF"]').click()
        time.sleep(.5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="eManualOptionTbody"]/tr[2]/td[3]/input')))
        driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[2]/td[3]/input').click()
        time.sleep(.5)
        action.send_keys("색상").perform()
        action.send_keys(Keys.TAB).perform()
        for i in range(len(color_)):
            action.send_keys(color_[i]).perform()
            action.send_keys(Keys.TAB).perform()
        time.sleep(.3)
        driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[3]/td[3]/input').click()
        action.send_keys("사이즈").perform()
        action.send_keys(Keys.TAB).perform()
        for i in range(len(size_)):
            action.send_keys(size_[i]).perform()
            action.send_keys(Keys.TAB).perform()
        time.sleep(.3)
        driver.find_element_by_xpath('//*[@id="eManualOptionCombine"]').click()
        action.send_keys(Keys.PAGE_DOWN).perform()

        num_op = len(color_)*len(size_)
        time.sleep(.5)
        if num_op > 9:
            for op in range(num_op):
                select = Select(driver.find_element_by_xpath(f'//*[@id="eItemList"]/table[{op+3}]/tbody/tr[1]/td[7]/select'))  # 검색종류
                select.select_by_visible_text('사용함')
                time.sleep(.3)
                driver.find_element_by_xpath(f'//*[@id="eItemList"]/table[{op+3}]/tbody/tr[1]/td[10]/input').click()
                action.send_keys("100").perform() # 0 이미 들어가 있음. 결국 1000됨.

        # 이미지 등록
        time.sleep(.5)
        if len(s) > 1:
            driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                down_path+fr"{j}_{subject_4f}/{subject_4f}_2_rs.jpg")
        else:
            driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                down_path+fr"{j}_{subject_4f}/{subject_4f}_1_rs.jpg")
        time.sleep(.5)

        # 추가 이미지 등록
        action.send_keys(Keys.PAGE_DOWN).perform()
        if len(s) > 1:
            for i in range(len(s)):
                if i==1 or i >=20:
                    continue
                driver.find_element_by_xpath('//*[@id="eOptionAddImageUpload"]').send_keys(down_path+fr"{j}_{subject_4f}/{subject_4f}_{i+1}_rs.jpg")
                time.sleep(.3)

        # 최종 상품등록
        time.sleep(.3)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="eProductRegister"]')))
        driver.find_element_by_xpath('//*[@id="eProductRegister"]').click()
        time.sleep(.7)
        alert = driver.switch_to.alert
        alert.accept()
        driver.switch_to.window(driver.window_handles[2])

        try:
            """driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div[3]/div[1]/span[1]/button[2]').click()
            time.sleep(.3)
            driver.find_element_by_xpath('//*[@id="eInputSearchSet"]').click()
            action.send_keys(category2).perform()

            action.send_keys(Keys.TAB).perform()
            action.send_keys(Keys.TAB).perform()
            action.send_keys(Keys.TAB).perform()
            action.send_keys(Keys.TAB).perform()
            action.send_keys(Keys.ENTER).perform()
            time.sleep(.5)"""

            btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[3]/div/button[1]') # 등록 버튼 클릭
            btn.click()

            time.sleep(15)
            alert = driver.switch_to.alert
            message = alert.text
            if message == '마켓으로 상품이 전송되었습니다.':
                alert.accept()
                print("마켓 전송 완료")
            else:
                alert.accept()
                driver.switch_to.window(driver.window_handles[2])
                driver.close()
                print("마켓 전송 실패!")

        except:
            driver.switch_to.window(driver.window_handles[2])
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
        action.send_keys(Keys.ESCAPE).perform() # 찜목록으로 재진입
        subject_list.append((subject, seller))
        n+=1
        print(f"{j}번째아이템 완료 ({n}개 업로드)")

    except:
        print(j, "번째아이템 오류")
        error.append(j-1) #index로 표시
        try:
            driver.switch_to.window(driver.window_handles[2])
            driver.close()  # 창닫기
        except:
            pass
        driver.switch_to.window(driver.window_handles[0])
        action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
        continue

    finally:
        # 이미지 폴더 삭제
        try:
            shutil.rmtree(down_path + f"{j}_{subject_4f}")
        except OSError as e:
            print(e.strerror)


print("완료된 상품 개수:", n)
print("error list: ", error)
print("finished")

