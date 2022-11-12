#상품 클릭

driver.find_element_by_xpath(
    '//*[@id="goods-detail-modal"]/div/div/div[1]/div/div[2]/div[2]/div[1]/button').click()  # 거래선으로 가기.. 없는 경우도 있다.
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
subject_ = driver.find_element_by_xpath(
    '// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text.strip()
subject_4f = subject_.replace("/", "-")
subject = back_data_mine.name_change(subject_)  # ops등 제목 수정

# 신상: 거래처따기 (새창- 3번째 창)
seller = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[1]/span').text.strip()
print("거래처: ", seller)

# 신상: 기본정보 따기 (새창- 3번째 창)
table = {}
datas = soup.find_all("div", attrs={'class': re.compile('w-full flex border-b border-gray-30')})
for data in datas:
    t_key = data.find("div", attrs={'class': re.compile('text-gray-80 border-r border-gray-30')}).get_text().strip()
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
# table['상품등록정보'] = table['상품등록정보'].replace(" ", "").split("등록")[0]

registered = table['상품등록정보']
category = table['카테고리'][1]
category2 = back_data_mine.category_convert[category]
if table['카테고리'][1] == '티&탑':  # 상품이름 입력시.. 변환 위함.. (오픈마켓에 &안들어감)
    category_ = '티-탑'
else:
    category_ = table['카테고리'][1]
color_ = table['색상']
size_ = table['사이즈']
subject = category_ + " " + subject
print("품명: ", subject)
print("table: ", table)

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
        p = re.compile('.*모델정보[^\n]*', re.DOTALL)
        m = p.search(r)
        comment = m.group()
        comment = comment.lower().replace("\n", "<br>")
        if "모델정보" not in comment:
            comment = ""
    except:
        r = ""
        comment = ""

# 신상:가격따기
price = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/span').text
price = int(re.sub(r'[^0-9]', '', price))
price_ = int(round((price * (1.133) + (300 + 1000)) / (1 - (.13 + .3)), -3))
if price_ % 10000 == 0:
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

"""# 하트 클릭
element = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/button')
action.move_to_element(element).perform()
element.click()
time.sleep(.3)"""

# 세번째 창 닫기
driver.close()  # 창닫기

############################# 입력 시작 ###################################3

# cafe24 상품등록으로 가기 (일반등록)
driver.switch_to.window(driver.window_handles[1])
time.sleep(.5)
driver.get("http://soyool.cafe24.com/disp/admin/shop1/product/productregister")  # new 관리자 - 등록
time.sleep(1)

# 진열상태, 판매상태 업데이트
wait.until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="QA_register1"]/div[2]/div/table/tbody/tr[1]/td/label[1]/input')))
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
driver.find_element_by_xpath('//*[@id="QA_register2"]/div[2]/div/table[1]/tbody/tr[2]/td/div[1]/input').click()
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

"""#중복 검사 (cafe24에 있는지..)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
val = soup.find("div", attrs={'class': 'tip', 'style': 'display: block;'})
if val:
    raise Exception("웹상에서 중복 확인")"""

# 상세설명 입력
html_template_ = "<h2>기본정보</h2><table><tbody>"
for i in table.keys():
    if i == '낱장 여부':
        continue
    html_template_ = html_template_ + f"<tr><td>{i}</td><td>{table[i]}</td></tr>"
html_template_ = html_template_ + f"</table></tbody><br><p>{comment}</p><br><p>더 다양한 상품을 soyool샵에서 만나보세요 :) </p><p>https://soyool.co.kr/</p><br>"

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

# 검색어 입력
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
wait.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "eOptionUseT"]')))
driver.find_element_by_xpath('// *[ @ id = "eOptionUseT"]').click()
time.sleep(.5)
wait.until(EC.element_to_be_clickable((By.XPATH, '// *[ @ id = "eUseOptionSetF"]')))
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
        select = Select(
            driver.find_element_by_xpath(f'//*[@id="eItemList"]/table[{op + 3}]/tbody/tr[1]/td[7]/select'))  # 검색종류
        select.select_by_visible_text('사용함')
        time.sleep(.3)
        driver.find_element_by_xpath(f'//*[@id="eItemList"]/table[{op + 3}]/tbody/tr[1]/td[10]/input').click()
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
    action.send_keys(category2).perform()

    action.send_keys(Keys.TAB).perform()
    action.send_keys(Keys.TAB).perform()
    action.send_keys(Keys.TAB).perform()
    action.send_keys(Keys.TAB).perform()
    action.send_keys(Keys.ENTER).perform()
    time.sleep(.5)

    btn = driver.find_element_by_xpath('//*[@id="footer"]/a[2]')  # 등록 버튼 클릭
    btn.click()

    # 마켓으로 보내기
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
action.send_keys(Keys.ESCAPE).perform()  # 찜목록으로 재진입

