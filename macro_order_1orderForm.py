import pandas as pd
import time
from openpyxl import load_workbook

print("order form 작성 시작")

sheet_order = 0 #(0~) 마스터의 몇번째 탭 import 할껀지 지정

timestr = time.strftime("%Y%m%d")
timestr_now = time.strftime("%Y%m%d-%H%M%S")
file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr+".xlsx"
df = pd.read_excel (file_name_master, sheet_name=sheet_order)

############################
#오더 양식으로 변경

#df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','shop_location', 'shop_phone_number','모델명'],dropna=False)[['수량','in_stock','구매수량']].sum()

df['option1'] = df['option1'].str.lower()
df['option2'] = df['option2'].str.lower()
df2 = df.groupby(['title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','building_name','shop_location', 'shop_phone_number','상품품목코드','모델명','note'],dropna=False).agg({'수량': 'sum','in_stock':'sum','구매수량':'sum'})
df2 = df2.add_suffix('').reset_index()
df2 = df2[df2['구매수량']>0]
df2 = df2[df2['note'] == "OK"]

cols = df2.columns.tolist()
cols = cols[:5]+cols[14:15]+cols[5:12]+cols[12:14]
df2 = df2[cols]

df2.insert(0,'고객사 상품코드_temp','')
df2.insert(1,'일시품절시_temp','')
df2.insert(6,'기타옵션-temp','')
df2.insert(9,'카테고리-temp','')
df2.insert(14,'blank1-temp','')
df2.insert(15,'blank2-temp','')
df2.insert(16,'blank3temp','')
df2.insert(17,'blank4-temp','')
df2.insert(19,'blank5-temp','')#메모2, 서율샵 자리

#공백 추가
df2.loc[-1]= ""
df2.index = df2.index + 1
df2 = df2.sort_index()

df2.loc[-1]= ""
df2.index = df2.index + 1
df2 = df2.sort_index()

file_order_form = "/Users/seoyulejo/Downloads/files/order_form_"+timestr+".xlsx"
if sheet_order == 0:
    df2.to_excel(file_order_form,index=False)
    print("엑셀 export 완료")
else:
    ExcelWorkbook = load_workbook(file_order_form)
    writer = pd.ExcelWriter(file_order_form, engine='openpyxl')
    writer.book = ExcelWorkbook
    df2.to_excel(writer, sheet_name=timestr_now, index=False)
    writer.save()
    writer.close()

