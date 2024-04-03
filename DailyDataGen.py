
import pandas as pd
from datetime import (datetime)
from RetailDataGen import (tran_hdr_daily ,tran_hdrCol,tran_dtl)

memberPath = r'/home/kiran/code/RetailProject/member_data.csv'
productPath = r'/home/kiran/code/RetailProject/product.csv'

memberFrame = pd.read_csv(memberPath, header=None, names=['id', 'name', 'surname', 'reg_storeId', 'reg_date'])
productFrame = pd.read_csv(productPath)
memberId = memberFrame['id'].tolist()
current_date = datetime.now().date()

tran_hdrFrame = pd.DataFrame(tran_hdr_daily(current_date,memberId),columns=tran_hdrCol)
tran_idDateList=tran_hdrFrame[['tran_id','purch_date']].values.tolist()
tran_dtlFrame = tran_dtl(tran_idDateList,productFrame)

# daily data files
path=r'/home/kiran/code/RetailProject/Data/'
hdrFile=f'{path}tran_hdr-{datetime.now()}.csv'
dtlFile=f'{path}tran_dtl-{datetime.now()}.csv'
with open(path+'.retail','a') as fs:
    fs.write(hdrFile+','+dtlFile+'\n')
tran_hdrFrame.to_csv(hdrFile,index=None)
tran_dtlFrame.to_csv(dtlFile,index=None)