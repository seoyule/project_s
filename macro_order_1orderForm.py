import macro_order_0master
import pandas as pd


############################
#오더 양식으로 변경
df = "여기 import 시키기"

df2 = df.groupby(['상품품목코드','note','title_ss','상품명(한국어 쇼핑몰)','option1','option2','price_ss','shop_name','shop_location', 'shop_phone_number','모델명'],dropna=False)[['수량','in_stock','구매수량']].sum()
df2.to_excel("/Users/seoyulejo/Downloads/files/order_form_"+timestr+".xlsx", index=False)
df_stock.to_excel("/Users/seoyulejo/Downloads/files/test.xlsx")


#timestr = time.strftime("%Y%m%d-%H%M%S")
#
#new_file_name = "order_master_"+timestr
#os.rename(file_name, "/Users/seoyulejo/Downloads/"+new_file_name)
