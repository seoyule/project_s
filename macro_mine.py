# for 변수: k,j,i
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

################################여기 입력해 주기###################################
urls = back_data.urls

start = [1] # 샵 중간부터 시작 시
number_d = 100 # 0일 경우 모든 상품, 지정하려면 숫자 입력

margin = .2
delivery_fee = 4000 #from 구매처:3000, to 고객:1000 (고객 부담 3000 -2000)
down_path = '/Users/seoyulejo/Downloads/imgs/'
###############################################################################

#기본세팅
warnings.filterwarnings("ignore")

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")

driver = webdriver.Chrome("/Users/seoyulejo/chromedriver", options=options) #, options=options
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
time.sleep(1)
# 광고 있으면 close
try:
    driver.find_element_by_class_name("btnClose.eClose").click()
    time.sleep(.3)
except:
    pass
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btnPromodeView')))
driver.find_element_by_class_name('btnPromodeView').click()# new 관리자 화면 진입 'newPromodeArea
time.sleep(.5)
print("cafe24 진입")

# 분류설정
category_list = back_data.category_list
driver.switch_to.window(driver.window_handles[0])

####################### 각 거래선 리뷰 시작 ##########################
error = []
for k in range(len(urls)):
    if start[0]>k:
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
    time.sleep(1)

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

    # 페이지 아래까지 한번 갔다오기
    for i in range(round(number*3 / 5)):
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(.2)
    action.send_keys(Keys.HOME).perform()
    print("스크롤 완료")

################# 신상마켓 거래선 총 상품목록 수집 ####################
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    goods_title = []
    goods_title_s = soup.find_all("div", attrs={"class": "ssm-image-detail-post goods-post"})

    if number*3 >= number_:
        num = number_
    else:
        num = number*3

    for i in range(num):
        if goods_title_s[i].find("div", attrs={"class": "sold-out"}):
            goods_title.append("sold-out")
        else:
            temp_name = goods_title_s[i].find("p", attrs = {"class":"post-content__title"}).get_text().strip()
            temp_name = back_data.name_change(temp_name)
            goods_title.append(temp_name)
    time.sleep(.5)
    print(f"신상-거래선 전체상품 list 완료: {len(goods_title)}개") # 거래처 전체 상품 목록 땀

################# cafe24 거래선 총 상품목록 수집 ####################
    driver.switch_to.window(driver.window_handles[1])

    # 상품목록 진입
    driver.get('https://crosschungdam.cafe24.com/disp/admin/shop1/product/productmanage')
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

    # 100개씩 보이게
    select = Select(driver.find_element_by_xpath('//*[@id="QA_list2"]/div[2]/div[2]/select[2]'))  # 검색종류
    select.select_by_visible_text('100개씩보기')
    time.sleep(1)

    # 목록 뽑기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    goods_list_s = soup.find_all("a", attrs={"class": "txtLink eProductDetail ec-product-list-productname"})
    goods_list = []
    for good in goods_list_s:
        goods_list.append(good.get_text())
    time.sleep(.5)

    if looping_num > 1:
        for loop in range(looping_num - 1):
            driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{loop + 2}]/a').click()  # 조회버튼 클릭
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html , 'html.parser')
            goods_list_s = soup.find_all("a" , attrs={"class": "txtLink eProductDetail ec-product-list-productname"})
            for good in goods_list_s:
                goods_list.append(good.get_text())
    print(f"cafe24-거래선 전체상품 list 완료: {len(goods_list)}개")

################### Cafe24에서 중단 상품 제거 ####################
    expired_ = []
    expired = []
    # expired_ 목록 산출 -100 단위로
    for i in range(len(goods_list)):
        if goods_list[i] in goods_title:
            pass
        else:
            expired_.append(i)

    if len(expired_) != 0:
        # expired 목록 작성 (0-99 단위)
        page = math.ceil((expired_[-1]+1)/100)
        for i in range(page):
            temp = [e - (i*100) for e in expired_ if e <(i+1)*100 and e > (i*100)-1]
            expired.append(temp) # [[0-99][100-199]...] -> [[0-99][00-99]...] 형식으로 나열
        print(f"expired 목록 작성 완료: 총{len(expired_)}개")

        # 뒷페이지부터 제거
        for i in reversed(range(page)):
            # 가장 뒷페이지 진입
            if len(expired[i]) == 0:
                continue
            driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[6]/ol/li[{i+1}]').click()
            time.sleep(1.5)
            # expired 틱
            for e in expired[i]:
                wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="product-list"]/tr[{e+1}]/td[1]/input')))
                element = driver.find_element_by_xpath(f'//*[@id="product-list"]/tr[{e+1}]/td[1]/input')
                action.move_to_element(element).perform()
                element.click()
                time.sleep(.3)
            # 삭제
            driver.find_element_by_xpath(f'//*[@id="QA_list2"]/div[5]/div[1]/a[6]').click()
            time.sleep(.3)
            alert = driver.switch_to.alert # 삭제확인 1
            alert.accept()
            time.sleep(.3)
            try:
                alert = driver.switch_to.alert # 삭제확인 2
                alert.accept()
            except:
                pass
            time.sleep(1.5)
        print(f"expired 상품 제거 완료: {len(expired_)}개")
    else:
        print("expired 상품 없음")
##################### Cafe24에 없는 상품 업데이트 ####################

    driver.switch_to.window(driver.window_handles[0])
    subject_list = [] #중복상품 스크린
    error_ = []

    for j in range(len(goods_title[:3])):  # len(goods_title[:number])로 재설정 하기

        # 이미 업데이트 유무/ 품절여부 확인
        if goods_title[j] in goods_list:
            continue
        if goods_title[j].lower() == "sold-out":
            continue
        # 가품 확인
        fake = False
        for f in back_data.fakes:
            if f in goods_title[j]:
                fake = True
                break
        if "x" in goods_title[j].lower():
            if "xl" in goods_title[j].lower():
                pass
            else:
                fake = True
        if fake:
            print("가품 skip: ", goods_title[j])
            continue
        # 중복확인
        if goods_title[j] in subject_list:
            print("동일상품 skip")
            continue

        try:
            j += 1
            print(k,"-",j, "번째아이템 시작")

            # 첫번째 창에서 아이템 클릭
            time.sleep(.5)
            driver.find_element_by_xpath(
                f'//*[@id="{id}"]/div/div[{location}]/div/div[2]/div/div/div[1]/div[{j}]/div[1]').click()
            time.sleep(1)
            addr = driver.current_url

            # 아이템화면 진입 (새창- 3번째 창)
            driver.switch_to.new_window('tab')
            driver.switch_to.window(driver.window_handles[2])
            driver.get(addr)
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.XPATH, '// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p')))

            # 소스 수집
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 제목따기
            subject_ = driver.find_element_by_xpath('// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text
            subject = subject_.strip()
            subject = back_data.name_change(subject) #ops등 제목 수정
            print("품명: ", subject_, subject)

            #검색어
            subject_keywords = subject.replace(" ", ",")
            subject_keywords = subject_keywords.split(",")
            subject_keywords = [subject_keyword[0:18] for subject_keyword in subject_keywords]
            subject_keywords = ",".join(subject_keywords)

            # 품절 다시한번 확인
            if soup.find("div", attrs={'class': 'sold-out'}):
                print("품절상품 skip")
                driver.close()  # 창닫기
                driver.switch_to.window(driver.window_handles[0])
                action.send_keys(Keys.ESCAPE).perform() # 찜목록으로 재진입
                continue

            """
            # 제품 상세설명 따기
            try:
                r = soup.find("div", attrs={"class": "row__content"}).get_text()
                r = r.replace("\n", "<br>")
                comment = r.split(dividor)[0]
            except:
                comment = ""
            """

            # 거래처따기
            seller = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').text.strip()
            print("거래처: ", seller)

            # 가격따기
            price = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/span').text
            price = int(re.sub(r'[^0-9]', '', price))
            price_ = int(round((price+delivery_fee)/(1-(.13+margin)), -3)) #https://docs.google.com/spreadsheets/d/1ZNMG8hey03UuLasNO5dEvQo1ncBi-GZXVQn6WP5EMZQ/edit#gid=289254889
            if price_ < 10000:
                price_ = 10000
            print("매입가/판매가: ", price, price_)

            # 분류 따기
            category = driver.find_element_by_xpath(
                '//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').text
            print("분류: ", category)

            # 등록일자
            try:
                registered = soup.find("div", string=" 상품등록정보 ").next_sibling.get_text()
                registered = registered.replace(" ","").split("등록")[0]
            except:
                registered = ""
            print("등록일자: ", registered)

            # 칼라따기 (리스트)
            color = driver.find_element_by_xpath(
                '//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]').text
            color.replace(" ", "")
            color_ = color.split(',')
            print("색상: ", color)

            # 사이즈따기 (리스트)
            size = driver.find_element_by_xpath(
                '//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]').text
            size.replace(" ", "")
            size_ = size.split(',')
            print("사이즈: ", size)

            # 이미지 다운로드
            r = soup.select_one('.swiper-wrapper')
            s = r.find_all("img")
            count = 0
            os.mkdir(down_path+f"{j}_{subject}")
            for i in s:
                link = i.attrs['src']
                #print(link)
                res = requests.get(link)
                if res.status_code == 200 and count < 20:
                    file_ = down_path+f"{j}_{subject}/{subject}_{count + 1}.jpg"
                    with open(file_, "wb") as file:
                        file.write(res.content)
                    if os.path.getsize(file_) > 2000000:
                        img = Image.open(file_)
                        img = img.convert('RGB')
                        img.save(file_, 'JPEG', qualty=85)
                count += 1
            print("이미지저장 완료")

            #세번째 창 닫기
            driver.close() #창닫기

            ############################# 입력 시작 ###################################3

            # cafe24 상품등록으로 가기 (일반등록)
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(.5)
            driver.get("http://crosschungdam.cafe24.com/disp/admin/shop1/product/productregister") # new 관리자 - 등록
            time.sleep(1)

            # 진열상태, 판매상태 업데이트
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[1]/td/label[1]/input')))
            driver.find_element_by_xpath('//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[1]/td/label[1]/input').click()
            driver.find_element_by_xpath('//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[2]/td/label[1]/input').click()
            time.sleep(.3)

            # 상품분류
            if urls[k][3].lower() == "yes":
                driver.find_element_by_xpath('//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[10]').click()
            else:
                try:
                    for i in range(len(category_list[category])):
                        driver.find_element_by_xpath(category_list[category][i]).click()
                        time.sleep(.3)
                except:
                    driver.find_element_by_xpath(
                        '//*[@id="eCategoryTbody"]/tr/td[1]/div/ul/li[11]').click()
            driver.find_element_by_xpath('//*[@id="eCategoryTbody"]/tr/td[5]/div').click() #등록

            # 상품명 입력
            time.sleep(.3)
            driver.find_element_by_xpath('//*[@id="product_name"]').click()
            action.send_keys(subject).perform()
            time.sleep(.2)
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[2]/td/div[1]/input').click()
            action.send_keys(subject_).perform() #원래 상품명: 영문상품명에 입력
            time.sleep(.2)
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[3]/td/input').click()
            action.send_keys(subject_[0:49]).perform()
            time.sleep(.3)

            # seller 공급사 상품명에 등록
            driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[4]/td/input').click()
            action.send_keys(seller[:240]).perform()
            time.sleep(.3)

            # 상세설명 입력
            html_template = f"""    
            <h2>기본정보</h2>
            <br>
            <table bgcolor="#D9E5FF" style="font-family: arial, sans-serif; border-collapse: collapse; font-size:120%;">
                <tbody>
                    <tr>
                        <td>카테고리</td>
                        <td>{category}</td>
                    </tr>
                    <tr>
                        <td>색상</td>
                        <td>{color}</td>
                    </tr>
                    <tr>
                        <td>사이즈</td>
                        <td>{size}</td>
                    </tr>
                    <tr>
                        <td>등록일자</td>
                        <td>{registered}</td>
                    </tr>
                </tbody>
            </table>
            <br>
            <p style="font-family: arial, sans-serif; font-size:120%;">더 다양한 상품을 <a style="text-decoration-line:underline; color: green;" href="http://chungdam-cross.co.kr">청담크로스</a>에서 만나보세요 :) </p>
            <p><a style="text-decoration-line:underline; color: green;" href="http://chungdam-cross.co.kr">http://chungdam-cross.co.kr</a></p>
            <br>
            """
            driver.find_element_by_xpath('//*[@id="eTabNnedit"]').click()
            driver.find_element_by_xpath('//*[@id="html-1"]').click()
            action.send_keys(html_template).perform()
            driver.find_element_by_xpath('//*[@id="html-1"]').click()
            driver.find_element_by_xpath('//*[@id="tabCont1_2"]/div/div/div[2]').click()
            for i in range(30):
                action.send_keys(Keys.ARROW_DOWN).perform()
            driver.find_element_by_xpath('//*[@id="insertFiles-1"]').click() # 다중이미지 클릭
            files = [] #파일선택
            for i in range(len(s)):
                if i<20:
                    files.append(down_path+f"{j}_{subject}/{subject}_{i + 1}.jpg")
            list_file = '\n'.join(files)
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="fr-files-upload-layer-1"]/div/div[2]/input').send_keys(list_file)
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="checkAll-1"]').click() #전체선택
            time.sleep(.5)
            driver.find_element_by_xpath('//*[@id="insertAll-1"]').click() #올리기
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

            # 이미지 등록
            #driver.find_element_by_xpath('//*[@id="imgRegisterContainer"]/ul/li[1]/span[4]/a[1]').click()
            #time.sleep(1)
            #pyautogui.press('escape')
            time.sleep(.5)
            if len(s) > 1:
                driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                    down_path+fr"{j}_{subject}/{subject}_2.jpg")
            else:
                driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
                    down_path+fr"{j}_{subject}/{subject}_1.jpg")
            time.sleep(.5)

            # 추가 이미지 등록
            action.send_keys(Keys.PAGE_DOWN).perform()
            if len(s) > 1:
                #driver.find_element_by_xpath('//*[@id="QA_register5"]/div[2]/div/table/tbody/tr[2]/td/div/div[1]/div[2]/a').click()
                #time.sleep(.5)
                #pyautogui.press('escape')
                for i in range(len(s)):
                    if i==1 or i >=20:
                        continue
                    driver.find_element_by_xpath('//*[@id="eOptionAddImageUpload"]').send_keys(down_path+fr"{j}_{subject}/{subject}_{i+1}.jpg")
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
                btn = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[3]/div/button[1]') # 등록 버튼 클릭
                btn.click()
                time.sleep(.7)
                alert = driver.switch_to.alert
                alert.accept()
            except:
                driver.close()

            driver.switch_to.window(driver.window_handles[0])
            action.send_keys(Keys.ESCAPE).perform() # 찜목록으로 재진입
            pyautogui.press('ctrl') # sleep 방지
            print(k, "-", j, "번째아이템 완료")
            subject_list.append(subject)
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
                shutil.rmtree(down_path + f"{j}_{subject}")
            except OSError as e:
                print("Error: %s : %s" % (down_path + f"{j}_{subject}", e.strerror))

    error.append(error_)

print("error list: ", error)
print("finished")

