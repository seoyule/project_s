import pandas as pd
import time

# df 점검사항: 1. soldout, url 없음
# 몇번째 탭 import 할껀지 지정 (0~)
sheet_order = 0

timestr = time.strftime("%Y%m%d")
file_name_master = "/Users/seoyulejo/Downloads/files/order_master_"+timestr+".xlsx"
df = pd.read_excel (file_name_master, sheet_name=0)

############################
#오더 양식으로 변경

#df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','shop_location', 'shop_phone_number','모델명'],dropna=False)[['수량','in_stock','구매수량']].sum()
df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','building_name','shop_location', 'shop_phone_number','모델명'],dropna=False).agg({'수량':'sum','in_stock':'sum','구매수량': 'sum'})
df2.to_excel("/Users/seoyulejo/Downloads/files/order_form_"+timestr+".xlsx")



#timestr = time.strftime("%Y%m%d-%H%M%S")
#
#new_file_name = "order_master_"+timestr
#os.rename(file_name, "/Users/seoyulejo/Downloads/"+new_file_name)
