import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from datetime import date as Date

#path
memberPath = r'./member_data.csv'
productPath = r'./product.csv'
transHeaderPath = r'./transHeader.csv'
transDetailPath = r'./transDetail.csv'

#read_csvs
members = pd.read_csv(memberPath,header=None,names=['member_id','f_name','l_name','store_id','trans_date'])
products =pd.read_csv(productPath)
transHeader = pd.read_csv(transHeaderPath)
transDetail = pd.read_csv(transDetailPath)

#Retail
#retail = transHeader.join(transDetail ,on='trans_id',how='inner')
retail = transHeader.merge(transDetail,on='trans_id',how='inner')
#retail['total']=retail.groupby(['member_id'])['amount'].transform('sum')
newRetail = retail.groupby(['member_id'])['amount'].sum()
newRetail=newRetail.sort_values(ascending=False)
#print(newRetail.amount)

#matplotlib
newRetail.plot(x="member_id",y="amount",kind="bar")
plt.show()