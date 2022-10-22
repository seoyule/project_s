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
from PIL import Image
import math
import back_data_mine
import pickle
from selenium import webdriver  # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# 기본세팅
start = 1 # 샵 중간부터 시작 시 (0 ~)
number_d = 200 # 0일 경우 모든 상품, 스크린 하려는 상품 개수
down_path = '/Users/seoyulejo/Downloads/imgs/'
error = []
subject_4f = ""

warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
driver.maximize_window()
driver.implicitly_wait(15)
action = ActionChains(driver)
wait = WebDriverWait(driver, 15)

category_list = back_data_mine.category_list # 분류설정
"""
with open('listfile', 'rb') as fp: # url 리스트 불러오기
    urls = pickle.load(fp)
"""
urls = [("https://sinsangmarket.kr/store/11711?isPublic=1","누죤 지하2층 706호 쵸콜릿","no"),
        ("https://sinsangmarket.kr/store/21781?isPublic=1","누죤 지하2층 213호 CC하니","no"),
        ("https://sinsangmarket.kr/store/7548?isPublic=1","스튜디오W 2층 36호 Ami 아미","no"),
        ("https://sinsangmarket.kr/store/14751?isPublic=1","디오트 지하2층 A07 블랙번","no"),
        ("https://sinsangmarket.kr/store/9765?isPublic=1","남평화 3층 127호 초이스(Choice)","no"),
        ("https://sinsangmarket.kr/store/8984?isPublic=1","누죤 지하1층 615호 오블리","no"),
        ("https://sinsangmarket.kr/store/2729?isPublic=1","디오트 2층 J06 헤르츠","no"),
        ]

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
time.sleep(.5)
"""try:
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
# 광고 있으면 close
try:
    driver.find_element_by_class_name("btnClose.eClose").click()
    time.sleep(.3)
except:
    pass
print("cafe24 진입")

driver.switch_to.window(driver.window_handles[0])

####################### 각 거래선 리뷰 시작 ##########################

for k in range(len(urls)): #len(urls)로 변경
    if start > k:
        continue
    # 신상마켓 리뷰 시작
    url = urls[k][0]
    # seller id 추출
    p = re.compile(r'sinsangmarket.kr/store/([0-9]+)')
    m = p.search(url)
    id = m.group(1)
    time.sleep(2)

    # seller 샵으로 들어가기
    time.sleep(.5)
    driver.get(url)
    time.sleep(.5)
    print("셀러샵 진입: ", id)
    time.sleep(3)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find("div",string = ' 매장 TOP 30 '):
        location = 3
    else:
        location = 2

    # 찜순/선택순
    if urls[k][2].lower() == "yes":
        url = url.split("?")
        url = url[0] + "?sort=likes&" + url[1]
        driver.get(url)
        print("찜순 선택")
        time.sleep(1)
    else:
        print("최신순 선택")

    # 수행 횟수 구하기
    number_ = driver.find_element_by_xpath(f'//*[@id="{id}"]/div/div[{location}]/div/div[1]/div[1]').text
    number_ = int(number_.split(" ")[1].split("개")[0].replace(",",""))
    if number_d == 0:
        number = number_
    elif number_d >= number_:
        number = number_
    else:
        number = number_d

    print("상품 개수: ", number_)
    print("루핑 횟수: ", number)

################# 신상마켓 거래선 총 상품목록 수집 ####################

################# cafe24 거래선 총 상품목록 수집 ####################
    driver.switch_to.window(driver.window_handles[1])

    # 상품목록 진입
    driver.get('https://soyool.cafe24.com/disp/admin/shop1/product/productmanage')
    time.sleep(1)
    select = Select(driver.find_element_by_xpath('//*[@id="eSearchFormGeneral"]/li/select[1]'))  # 검색종류 - 공급사
    select.select_by_visible_text('공급사 상품명')
    time.sleep(.3)
    driver.find_element_by_xpath('//*[@id="eSearchFormGeneral"]/li/input').click()  # 검색창클릭
    time.sleep(.3)
    action.send_keys(urls[k][1]).perform() # 거래선 이름 인풋
    time.sleep(.3)
    driver.find_element_by_xpath('//*[@id="eBtnSearch"]').click()  # 조회버튼 클릭
    time.sleep(1)

    # 상품 목록 출력
    num_goods = driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[1]/p').text
    num_goods = int(num_goods.split(" ")[1].split("개")[0])
    looping_num = num_goods / 100
    looping_num = math.ceil(looping_num)
    print("총", num_goods, "개")
    print("페이지", looping_num, "개")

    # 100개씩 보이게
    select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]'))  # 검색종류
    select.select_by_visible_text('100개씩보기')
    time.sleep(1)

    # 기본-cafe24: 목록 뽑기 (goods_list)
    goods_list = []
    for loop in range(1): #looping_num
        if loop % 10 == 0 and loop != 0:  # next page 버튼 누르기
            if loop == 10:
                element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a')
            else:
                element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/a[2]')
            action.move_to_element(element)
            element.click()
            time.sleep(4)

        element = driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop % 10 + 1}]')  # 페이지 번호버튼 클릭
        page = element.text
        element.click()
        print(page, "페이지 시작!!")
        time.sleep(2)

        if loop == looping_num - 1:
            num = num_goods - ((looping_num - 1) * 100)
        else:
            num = 100

        for i in range(num):
            t_name = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{i + 1}]/td[5]/div/p/a').text
            goods_list.append(t_name)

    print(f"cafe24-거래선 전체상품 list 완료: {len(goods_list)}개")

##################### Cafe24에 상품 업데이트 ####################
    driver.switch_to.window(driver.window_handles[0])
    subject_list = [] #중복상품 스크린
    error_ = []
    existing = 0
    n = 0  # 완료된 상품 개수

    for j in range(number):
        if existing > 10:
            print("cafe24 - 이전 업데이트 포인트 도달")
            break
        try:
            j += 1
            print(k,"-",j, "번째아이템 시작")

            # 신상: 아이템 클릭 (첫번째 창)
            pyautogui.press('ctrl')  # sleep 방지
            time.sleep(.5)
            driver.find_element_by_xpath(
                f'//*[@id="{id}"]/div/div[{location}]/div/div[2]/div/div/div[1]/div[{j}]/div[1]').click()
            time.sleep(1)
            addr = driver.current_url

            # 신상: 아이템화면 진입 (새창- 3번째 창)
            driver.switch_to.new_window('tab')
            driver.switch_to.window(driver.window_handles[2])
            driver.get(addr)
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p')))

            # 신상: 소스 수집 (새창- 3번째 창)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 신상: 제목따기 (새창- 3번째 창)
            subject_ = driver.find_element_by_xpath(
                '// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text.strip()
            subject_4f = subject_.replace("/", "-")
            subject = back_data_mine.name_change(subject_)  # ops등 제목 수정

            # 신상: 거래처따기 (새창- 3번째 창)
            seller = driver.find_element_by_xpath(
                '//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').text.strip()
            print("거래처: ", seller)

            # 신상: 기본정보 따기 (새창- 3번째 창)
            table = {}
            datas = soup.find_all("div", attrs={'class': re.compile('w-full flex border-b border-gray-30')})
            for data in datas:
                t_key = data.find("div", attrs={
                    'class': re.compile('text-gray-80 border-r border-gray-30')}).get_text().strip()
                t_value = data.find("div", attrs={'class': re.compile('text-gray-100')})
                if t_value:
                    if len(t_value) > 1:
                        t_val = []
                        for i in t_value:
                            t_val.append(i.get_text().strip())
                    else:
                        t_val = t_value.get_text().strip()
                    table[t_key] = t_val

            color = table['색상']
            table['색상'] = table['색상'].replace(" ", "").split(',')
            size = table['사이즈']
            table['사이즈'] = table['사이즈'].lower().replace("sml", "S,M,L")
            table['사이즈'] = table['사이즈'].replace(" ", "").split(',')
            if table['사이즈'][0] == 'F':
                table['사이즈'][0] = 'Free'
            #table['상품등록정보'] = table['상품등록정보'].replace(" ", "").split("등록")[0]

            registered = table['상품등록정보']
            category = table['카테고리'][1]
            if table['카테고리'][1] == '티&탑':  # 상품이름 입력시.. 변환 위함.. (오픈마켓에 &안들어감)
                category_ = '티-탑'
            else:
                category_ = table['카테고리'][1]
            color_ = table['색상']
            size_ = table['사이즈']
            subject = category + " " + subject
            print("품명: ", subject)
            print("table: ", table)

            # 신상: 기존 cafe24업로드 여부 확인 (새창- 3번째 창)
            if subject in goods_list:
                existing += 1
                print("cafe24에 이미있음 skip: ", subject)
                driver.close()  # 창닫기
                driver.switch_to.window(driver.window_handles[0])
                action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
                continue

            """# 신상: 등록일자 비교
            x = table['상품등록정보']
            first = datetime(int(x[:4]), int(x[5:7]), int(x[8:]))
            dt_now = datetime.now()
            second = dt_now + relativedelta(months=-6)
            if second >= first:
                print("6개월이상 지난상품 skip: ", x)
                driver.close()  # 창닫기
                driver.switch_to.window(driver.window_handles[0])
                action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
                continue"""

            """# 신상: 낱장여부 확인 (새창- 3번째 창)
            if table['낱장 여부'] != '낱장 가능':
                print("낱장 안됨 skip: ", subject)
                driver.close()  # 창닫기
                driver.switch_to.window(driver.window_handles[0])
                action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
                continue"""

            # 낱장 셀러 등록 - 생략

            # 신상: 가품 확인 (새창- 3번째 창)
            fake = False
            for f in back_data_mine.fakes:
                if f in subject:
                    fake = True
                    break
            if "x" in subject.lower():
                if "xl" in subject.lower():
                    pass
                else:
                    fake = True
            if fake:
                print("가품 skip: ", subject)
                driver.close()  # 창닫기
                driver.switch_to.window(driver.window_handles[0])
                action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
                continue

            # 신상: 중복업데이트확인 (새창- 3번째 창)
            if subject in subject_list:
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
                action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입
                continue

            # 신상: 검색어
            subject_keywords = subject.replace(", ", ",")
            subject_keywords = subject_keywords.replace(" ", ",")
            subject_keywords = subject_keywords.replace("(", ",")
            subject_keywords = subject_keywords.replace(")", ",")
            subject_keywords = subject_keywords.split(",")
            subject_keywords = [subject_keyword[0:18] for subject_keyword in subject_keywords]
            subject_keywords = ",".join(subject_keywords)

            # 신상: 제품 상세설명 따기 - 생략

            # 신상: 이미지 사용가능 여부 체크
            image_avail = ""
            r = soup.find("div", attrs={"class": "row__content"}).get_text()
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
            price = driver.find_element_by_xpath(
                '//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/span').text
            price = int(re.sub(r'[^0-9]', '', price))
            price_ = int(round((price * (1.133) + (300 + 1000)) / (1 - (.13 + .3)),-3))
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
                        resized_img = Image.new(mode='RGB', size=(size, size),color = "white")
                        offset = (round((abs(x - size)) / 2), round((abs(y - size)) / 2))
                        resized_img.paste(img, offset)
                        resized_img.save(file_rs)
                count += 1
            print("이미지저장 완료")

            #세번째 창 닫기
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
            driver.find_element_by_xpath('//*[@id="eCategoryTbody"]/tr/td[5]/div').click()  # 등록

            # 상품명 입력
            time.sleep(.3)
            driver.find_element_by_xpath('//*[@id="product_name"]').click()
            action.send_keys(subject).perform()
            time.sleep(.2)
            driver.find_element_by_xpath(
                '//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[2]/td/div[1]/input').click()
            action.send_keys(subject_).perform()  # 원래 상품명: 영문상품명에 입력
            time.sleep(.2)

            # 등록일 입력 - 상품명(관리용)에..
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[3]/td/input').click()
            action.send_keys(table.get('상품등록정보')).perform()
            time.sleep(.3)

            # seller - url 공급사 상품명에 등록
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[4]/td/input').click()
            action.send_keys(seller, " ", addr).perform()
            time.sleep(.3)

            # url 모델명에 등록
            driver.find_element_by_xpath('//*[@id="eProductModelName"]').click()
            action.send_keys(addr).perform()
            time.sleep(.3)

            # seller 자체 상품코드에 등록
            driver.find_element_by_xpath('//*[@id="ma_product_code"]').click()
            action.send_keys(seller[:39]).perform()
            time.sleep(.5)

            # 상세설명 입력
            html_template_ = "<h2>기본정보</h2><table><tbody>"
            for i in table.keys():
                if i == '낱장 여부':
                    continue
                html_template_ = html_template_ + f"<tr><td>{i}</td><td>{table[i]}</td></tr>"
            html_template_ = html_template_ + f"</table></tbody><br><p>더 다양한 상품을 soyool샵에서 만나보세요 :) </p><p>https://soyool.co.kr/</p><br>"

            driver.find_element_by_xpath('//*[@id="eTabNnedit"]').click()
            driver.find_element_by_xpath('//*[@id="html-1"]').click()
            action.send_keys(html_template_).perform()
            driver.find_element_by_xpath('//*[@id="html-1"]').click()
            driver.find_element_by_xpath('//*[@id="tabCont1_2"]/div/div/div[2]').click()
            for i in range(30):
                action.send_keys(Keys.ARROW_DOWN).perform()
            driver.find_element_by_xpath('//*[@id="insertFiles-1"]').click()  # 다중이미지 클릭
            files = []  # 파일선택
            for i in range(len(s)):
                if i < 20:
                    files.append(down_path + f"{j}_{subject_4f}/{subject_4f}_{i + 1}.jpg")
            list_file = '\n'.join(files)
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="fr-files-upload-layer-1"]/div/div[2]/input').send_keys(list_file)
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="checkAll-1"]').click()  # 전체선택
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="insertAll-1"]').click()  # 올리기
            time.sleep(.5)

            #검색어 입력
            wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="QA_register2"]/div[2]/div/table[2]/tbody/tr/td/div/input'))).click()
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[2]/tbody/tr/td/div/input').click()
            action.send_keys(subject_keywords[:49]).perform()

            # 가격입력
            action.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="product_price"]').click()
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

            num_op = len(color_) * len(size_)
            time.sleep(.5)
            if num_op > 9:
                for op in range(num_op):
                    select = Select(driver.find_element_by_xpath(
                        f'//*[@id="eItemList"]/table[{op + 3}]/tbody/tr[1]/td[7]/select'))  # 검색종류
                    select.select_by_visible_text('사용함')
                    time.sleep(.5)
                    driver.find_element_by_xpath(
                        f'//*[@id="eItemList"]/table[{op + 3}]/tbody/tr[1]/td[10]/input').click()
                    action.send_keys("100").perform()  # 0 이미 들어가 있음. 결국 1000됨.

            # 이미지 등록
            time.sleep(.5)
            if len(s) > 1:
                driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                    down_path + fr"{j}_{subject_4f}/{subject_4f}_2_rs.jpg")
            else:
                driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                    down_path + fr"{j}_{subject_4f}/{subject_4f}_1_rs.jpg")
            time.sleep(.5)

            # 추가 이미지 등록
            action.send_keys(Keys.PAGE_DOWN).perform()
            if len(s) > 1:
                for i in range(len(s)):
                    if i == 1 or i >= 20:
                        continue
                    driver.find_element_by_xpath('//*[@id="eOptionAddImageUpload"]').send_keys(
                        down_path + fr"{j}_{subject_4f}/{subject_4f}_{i + 1}_rs.jpg")
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
                driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div[3]/div[1]/span[1]/button[2]').click()
                time.sleep(.3)
                driver.find_element_by_xpath('//*[@id="eInputSearchSet"]').click()
                action.send_keys(category).perform()

                action.send_keys(Keys.TAB).perform()
                action.send_keys(Keys.TAB).perform()
                action.send_keys(Keys.TAB).perform()
                action.send_keys(Keys.TAB).perform()
                action.send_keys(Keys.ENTER).perform()
                time.sleep(.5)

                btn = driver.find_element_by_xpath('//*[@id="footer"]/a[2]')  # 등록 버튼 클릭
                btn.click()

                try:
                    time.sleep(6)
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    time.sleep(6)
                    driver.find_element_by_xpath('//*[@id="layerImpossible"]/div[2]/a[1]').click()
                    time.sleep(.5)
                    alert = driver.switch_to.alert
                    alert.accept()

            except:
                driver.close()

            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform() # 찜목록으로 재진입
            subject_list.append(subject)
            n+=1
            print(k, "-", j, f"번째아이템 완료({n}개 업로드)")

        except:
            print(k,"-",j, "번째아이템 오류")
            error_.append(j-1)#index로 표시
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

    error.append(error_)

print("error list: ", error)
print("finished")

