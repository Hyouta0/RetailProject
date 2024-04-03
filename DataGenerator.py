from datetime import (timedelta, datetime, time)
import pandas as pd
from RetailDataGen import (tran_hdr,tran_dtl)

memberPath = r'./member_data.csv'
productPath = r'./product.csv'

memberFrame = pd.read_csv(memberPath, header=None, names=['id', 'name', 'surname', 'reg_storeId', 'reg_date'])
productFrame = pd.read_csv(productPath)
memberId = memberFrame['id'].tolist()
current_date = datetime.now().date()
begining_date = current_date.replace(year=current_date.year - 3)

tran_hdrFrame = tran_hdr(begining_date,current_date,memberId)
tran_idDateList = tran_hdrFrame[['tran_id','purch_date']].values.tolist()
tran_dtlFrame=tran_dtl(tran_idDateList,productFrame)

tran_hdrFrame.to_csv('./tran_hdr.csv',index=None)
tran_dtlFrame.to_csv('./tran_dtl.csv',index=None)

