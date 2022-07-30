
from bs4 import BeautifulSoup # 파싱된 데이터를 python에서 사용하기 좋게 변환
from selenium import webdriver # webdriver를 통해 파싱하기 위함
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import time
import requests
import pyautogui


driver = webdriver.Chrome("/Users/seoyulejo/chromedriver")
driver.implicitly_wait(15)
url = 'https://sinsangmarket.kr/'
driver.get(url)
driver.maximize_window()
action= ActionChains(driver)

#신상마켓 로그인
driver.find_element_by_class_name("px-6px").click()
time.sleep(.5)
action.send_keys('chanelj77').perform()
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[2]/input').click()
action.send_keys('crosscd123!').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div/button').click()


#광고 있으면 close
time.sleep(4)
try:
    ad = driver.find_element_by_class_name("button.close-button")
    ad.click()
except:
    pass

#한글로 바꾸기
time.sleep(1)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/div').click()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[5]/div/ul/li[1]/label').click()
time.sleep(1)

try:
    ad = driver.find_element_by_class_name("button.close-button")
    ad.click()
except:
    pass

#찜 목록으로 들어가기
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[1]/div/ul/li[3]/a/span').click()
time.sleep(2)

#페이지 아래까지 한번 갔다오기
prev_height= driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    curr_height= driver.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break
    prev_height = curr_height

action.send_keys(Keys.HOME).perform()
print("스크롤 완료")

#실행 횟수
number_ = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div/div/section/article/div/button').text
number = int(number_.split('/')[1].split(')')[0])
print(number)

#cafe24 열기
driver.execute_script('window.open("https://eclogin.cafe24.com/Shop/");')
time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
time.sleep(1)
driver.find_element_by_xpath('//*[@id="mall_id"]').click()
time.sleep(.5)
action.send_keys('crosschungdam').perform()
driver.find_element_by_xpath('//*[@id="userpasswd"]').click()
action.send_keys('crosscd123').perform()
time.sleep(.5)
driver.find_element_by_xpath('//*[@id="frm_user"]/div/div[3]/button').click()
time.sleep(5)


# 분류작업
category_list = {
    '신상품': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[1]'],
    '원피스': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[2]'],
    '셔츠/남방': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
              '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[1]'],
    '블라우스': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
             '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[2]'],
    '니트': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[3]'],
    '티&탑': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[4]'],
    '빅사이즈': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
             '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[5]'],
    '임부복': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[3]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[6]'],
    '스커트': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[4]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[1]'],
    '청바지': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[4]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[2]'],
    '팬츠': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[4]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[3]'],
    '아우터': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[5]'],
    '세트 아이템': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[6]'],
    '샌들/슬리퍼/쪼리': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
                   '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[1]'],
    '플랫/로퍼': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
              '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[2]'],
    '힐/펌프스': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
              '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[3]'],
    '웨지힐': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[4]'],
    '스니커즈/운동화': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
                 '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[5]'],
    '워커/부츠': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
              '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[6]'],
    '수제화': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[7]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[7]'],
    '주얼리': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[1]'],
    '벨트': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[2]'],
    '헤어핀/밴드': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
               '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[3]'],
    '모자': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[4]'],
    '선그라스/안경': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
                '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[5]'],
    '시계': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[8]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[6]'],
    '가죽': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[1]'],
    '숄더백': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[2]'],
    '토트백': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
            '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[3]'],
    '크로스백': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
             '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[4]'],
    '클러치/지갑': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
               '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[5]'],
    '백팩': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[9]',
           '//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/div/ul/li[6]'],
    '남성의류': ['//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[10]']}


#루핑시작
for j in range(number): #number로 재설정 하기
    j += 1
    # cafe24 상품등록으로 가기
    time.sleep(.5)
    driver.get("http://crosschungdam.cafe24.com/disp/admin/shop1/product/ProductSimpleRegister")
    time.sleep(.5)

    #신상마켓으로 이동
    driver.switch_to.window(driver.window_handles[0])
    # 아이템화면 진입
    driver.find_element_by_xpath(
    f'//*[@id="app"]/div[1]/div[2]/div/div/section/div/article/div[{j}]/div[1]/div[1]').click()
    time.sleep(1)

    #소스 수집
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #제목따기
    subject = driver.find_element_by_xpath('// *[ @ id = "goods-detail"] / div / div[2] / div[2] / div[1] / p').text
    print(subject)
    # 가격따기
    price = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[2]/div[1]/div[3]/div[1]/span').text
    price = int(re.sub(r'[^0-9]', '', price))
    price_ = int(round(price*2*0.9,-3))
    print(price)
    #분류 따기
    category = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]').text
    print(category)
    #등록일자
    registered = soup.find("div", string=" 상품등록정보 ").next_sibling.get_text()
    print(registered)

    # 칼라따기 (리스트)
    color = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]').text
    color.replace(" ","")
    color_ =color.split(',')
    print(color)
    # 사이즈따기 (리스트)
    size = driver.find_element_by_xpath('//*[@id="goods-detail"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[3]/div[2]').text
    size.replace(" ", "")
    size_ = size.split(',')
    print(size)

    # 상세페이지 작성
    html_template = f"""    
<h2>기본정보</h2>
<br>
<table bgcolor="#D9E5FF" style="font-family: arial, sans-serif; border-collapse: collapse; width: 500px; font-size:150%;">
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
<br>
<br>
    """

    # 이미지 다운로드
    r = soup.select_one('.swiper-wrapper')
    s = r.find_all("img")

    count=0
    os.mkdir(f"/Users/seoyulejo/Downloads/imgs/{j}_{subject}")
    for i in s:
        link = i.attrs['src']
        html_template = html_template + f"""
        \n
        <div><img src='{link}'></div><br><br><br>
        \n
        """
        print(link)
        res = requests.get(link)
        if res.status_code == 200 and count<2:
            with open(f"/Users/seoyulejo/Downloads/imgs/{j}_{subject}/{subject}_{count + 1}.jpg", "wb") as file:
                file.write(res.content)
        count+=1


    time.sleep(.5)
    #찜목록으로 재진입
    action.send_keys(Keys.ESCAPE).perform()
    time.sleep(.5)

    # 카페24로 이동
    driver.switch_to.window(driver.window_handles[1])

    # 상품명 입력
    driver.find_element_by_xpath('//*[@id="product_name"]').click()
    action.send_keys(subject).perform()
    time.sleep(.5)
    # 상세설명 입력
    driver.find_element_by_xpath('//*[@id="html-1"]').click()
    action.send_keys(html_template).perform()
    time.sleep(.5)
    #가격입력
    driver.find_element_by_xpath('//*[@id="product_price"]').click()
    action.send_keys(price_).perform()
    time.sleep(.5)
    #진열상태, 판매상태 업데이트
    driver.find_element_by_xpath('//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[1]/td/div/label[1]/input').click()
    driver.find_element_by_xpath('//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[2]/td/div/label[1]/input').click()
    time.sleep(.5)
    #상품분류
    try:
        for i in range(len(category_list[category])):
            driver.find_element_by_xpath(category_list[category][i]).click()
            time.sleep(.5)
    except:
        driver.find_element_by_xpath('//*[@id="QA_register3"]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr/td[1]/div/ul/li[11]').click()

    #옵션설정
    time.sleep(.5)
    driver.find_element_by_xpath('// *[ @ id = "eOptionUseT"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('// *[ @ id = "eUseOptionSetF"]').click()

    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[2]/td[3]/input').click()
    action.send_keys("색상").perform()
    action.send_keys(Keys.TAB).perform()
    for i in range(len(color_)):
        time.sleep(.5)
        action.send_keys(color_[i]).perform()
        time.sleep(.5)
        action.send_keys(Keys.TAB).perform()

    time.sleep(.5)
    driver.find_element_by_xpath('//*[@id="eManualOptionTbody"]/tr[3]/td[3]/input').click()
    action.send_keys("사이즈").perform()
    action.send_keys(Keys.TAB).perform()
    for i in range(len(size_)):
        time.sleep(.5)
        action.send_keys(size_[i]).perform()
        time.sleep(.5)
        action.send_keys(Keys.TAB).perform()

    action.send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(.5)
    driver.find_element_by_xpath('// *[ @ id = "eOptionInputPanel"] / div[3] / div / a').click()
    time.sleep(1)

    #이미지 등록
    driver.find_element_by_xpath('//*[@id="QA_register5"]/div[2]/div/table/tbody/tr/td/div/div/div[1]/span[5]/a[1]').click()
    time.sleep(1)
    pyautogui.press('escape')
    time.sleep(.5)
    if len(s)>1:
        driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(fr"/Users/seoyulejo/Downloads/imgs/{j}_{subject}/{subject}_2.jpg")
    else:
        driver.find_element_by_xpath('//*[@id="imageFiles"]').send_keys(
            fr"/Users/seoyulejo/Downloads/imgs/{j}_{subject}/{subject}_1.jpg")
    time.sleep(.5)


    #상품등록
    driver.find_element_by_xpath('//*[@id="eProductRegisterForm"]/div[7]/a[1]').click()
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)



"""print("finished")
driver.close()
"""