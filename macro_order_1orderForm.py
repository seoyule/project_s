import pandas as pd
import time
from openpyxl import load_workbook

print("order form 작성 시작")
# df 점검사항: 1. soldout, url 없음
# 같은 구매자가 깔별로 구매하는지 확인 - 이런 경우 한개만 남기고 취소
# 몇번째 탭 import 할껀지 지정 (0~)
sheet_order = 0

timestr = time.strftime("%Y%m%d")
timestr_now = time.strftime("%Y%m%d-%H%M%S")
file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr+".xlsx"
df = pd.read_excel (file_name_master, sheet_name=sheet_order)

############################
#오더 양식으로 변경

#df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','shop_location', 'shop_phone_number','모델명'],dropna=False)[['수량','in_stock','구매수량']].sum()
df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','building_name','shop_location', 'shop_phone_number','모델명'],dropna=False).agg({'수량':'sum','in_stock':'sum','구매수량': 'sum'})

file_order_form = "/Users/seoyulejo/Downloads/files/order_form_"+timestr+".xlsx"
if sheet_order == 0:
    df2.to_excel(file_order_form)
    print("엑셀 export 완료")
else:
    ExcelWorkbook = load_workbook(file_order_form)
    writer = pd.ExcelWriter(file_order_form, engine='openpyxl')
    writer.book = ExcelWorkbook
    df2.to_excel(writer, sheet_name=timestr_now)
    writer.save()
    writer.close()
