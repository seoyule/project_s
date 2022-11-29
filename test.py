

"""
#0번파일
#미송 마스터에 반영
print("딜리버드 진입 - 미송 확인 (사입현황 탭)")
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').send_keys(Keys.ENTER) #재고로 가기
time.sleep(2)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[1]/div[1]/ul/li[3]/a').send_keys(Keys.ENTER) #미송상품 클릭
time.sleep(3)
driver.find_element_by_xpath('//*[@id="prepaidProduct_wrapper"]/div[1]/div[2]/div/button').send_keys(Keys.ENTER) # 엑셀 다운로드
time.sleep(4)

files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name3 = files[-1]

time.sleep(1)
df_delay = pd.read_excel(file_name3)
df_delay = df_delay[df_delay['진행 상태']=='진행중']
df_delay['미송대기수량'] = df_delay['사입 요청 수량']-df_delay['누적 사입 수량']-df_delay['환불 수량']
df_delay['상품옵션'] = df_delay['옵션 1/2'].str.replace('/','_')

df_delay['key'] = df_delay['판매 상품명']+"_"+df_delay['상품옵션']
df_delay['key'] = df_delay['key'].str.lower()
df_delay['key'] = df_delay['key'].replace('\s','', regex=True)

df_delay_ = df_delay[['key','미송대기수량','사입사 메모']]
list_d = df_delay_.values.tolist()
dict_d = {}
for i in range(len(list_d)):
    dict_d[list_d[i][0]] = [list_d[i][1],list_d[i][2]]
print("미송 dic 완료")

# 미송 - 매입 수량에서 제외..
p_number = [] # 미송 수량
note_misong = [] # 미송 노트
for i in range(len(df)):
    num = 0 #수량
    m_note =""
    if df['key'][i] in dict_d:
        if dict_d[df['key'][i]][0]>0:
            #stock 개수 넣기
            for j in range(df['구매수량'][i].item()):
                if dict_d[df['key'][i]][0]>0: #재고개수 >0?
                    num +=1
                    dict_d[df['key'][i]][0] -= 1
            m_note = dict_d[df['key'][i]][1]
    p_number.append(num)
    note_misong.append(m_note)
df['미송수량'] = p_number
df['실구매수량'] = df['구매수량']-df['미송수량']
df['미송노트'] = note_misong
print("df에 미송수량 반영")"""

#2번 파일
"""
print('사입+미송+반품 작성, 딜리버드 진입 - 상품 및 재고 탭')
#재고로 가기
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[7]/a').send_keys(Keys.ENTER)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[2]/div/div/div/div[3]/div/div/div[2]/label').send_keys(Keys.SPACE) #재고 없음 클릭
time.sleep(3)
driver.find_element_by_xpath('//*[@id="productList_wrapper"]/div[1]/div[2]/div/button[1]').send_keys(Keys.ENTER)
time.sleep(4)

files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name2 = files[-1]

time.sleep(1)
df_stock = pd.read_excel(file_name2)
df_stock['key'] = df_stock['판매 상품명']+"_"+df_stock['상품옵션 1']+"_"+df_stock['상품옵션 2']
df_stock['key'] = df_stock['key'].str.lower()
df_stock['key'] = df_stock['key'].replace('\s','', regex=True)

df_stock_ = df_stock[['key','상품번호','정상재고']]
list_ = df_stock_.values.tolist()
dict_ = {}
for i in range(len(list_)):
    dict_[list_[i][0]] = [list_[i][1],list_[i][2]]
print("사입+미송+반품 dic 완료")

# 반품 재고 매입 수량에 반영..
p_result = [] # 상품번호
p_number = [] # stock 수량
for i in range(len(df)):
    result = '' #번호
    num = 0 #수량
    if df['key'][i].lower() in dict_:
        # 상품번호 넣기
        result = dict_[df['key'][i].lower()][0]
        if dict_[df['key'][i].lower()][1]>0:
            #stock 개수 넣기
            for j in range(df['수량'][i].item()):
                if dict_[df['key'][i].lower()][1]>0: #재고개수 >0?
                    num +=1
                    dict_[df['key'][i].lower()][1] -= 1

    p_result.append(result)
    p_number.append(num)

df['사입번호'] = p_result
df['사입+미송+반품'] = p_number
df['수량check'] = df['수량']==df['사입+미송+반품']

#미송노트 마스터에 반영
print("딜리버드 진입 - 미송 확인 (사입현황 탭)")
driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/ul/li[2]/a').send_keys(Keys.ENTER) #사입현황으로 가기
time.sleep(2)
driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[1]/div[1]/ul/li[3]/a').send_keys(Keys.ENTER) #미송상품 클릭
time.sleep(3)
try:
    driver.find_element_by_xpath('//*[@id="page-wrapper"]/div[2]/div[1]/div[3]/div/div/div/form/div[2]/div[2]/label/span').click() #미송지연 클릭해제
    time.sleep(3)
except:
    driver.find_element_by_xpath(
        '//*[@id="page-wrapper"]/div[2]/div[1]/div[3]/div/div/div/form/div[2]/div[2]/label/span').click()
    time.sleep(3)
driver.find_element_by_xpath('//*[@id="prepaidProduct_wrapper"]/div[1]/div[2]/div/button').send_keys(Keys.ENTER) # 엑셀 다운로드
time.sleep(4)

files = list(filter(os.path.isfile, glob.glob(search_dir + "*")))
files.sort(key=lambda x: os.path.getmtime(x))
file_name3 = files[-1]

time.sleep(1)
df_delay = pd.read_excel(file_name3)

df_delay['상품옵션'] = df_delay['옵션 1/2'].str.replace('/','_')

df_delay['key'] = df_delay['판매 상품명']+"_"+df_delay['상품옵션']
df_delay['key'] = df_delay['key'].str.lower()
df_delay['key'] = df_delay['key'].replace('\s','', regex=True)

df_delay_ = df_delay[['key','사입사 메모']]
list_d = df_delay_.values.tolist()
dict_d = {}
for i in range(len(list_d)):
    dict_d[list_d[i][0]] = [list_d[i][1]]
print("미송 dic 완료")

# 미송노트 작성
note_misong = [] # 미송 노트
for i in range(len(df)):
    m_note =""
    if df['미송수량'][i]>0 and df['key'][i] in dict_d:
        m_note = dict_d[df['key'][i]][0]
    note_misong.append(m_note)
df['미송노트_'] = note_misong
print("df에 미송노트 반영")


try:
    os.remove(file_name2)
except OSError as e:
    print(e.strerror)



"""
