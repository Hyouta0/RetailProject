import pandas as pd
from datetime import date as dt

# path cfg
memberPath =r'./memberData.csv'
productPath =r'./product.csv'
transHeaderPath = r'./transHeader.csv'
transDetailsPath = r'./transDetails.csv'

# creating data frames
members = pd.read_csv(memberPath)
product = pd.read_csv(productPath)
transHeader = pd.read_csv(transHeaderPath)
transDetails = pd.read_csv(transDetailsPath)



# renaming columns name to make them same
members.rename(columns={'Id':'member_id','Fname':'f_name','Lname':'l_name','Date':'date'},inplace=True)
transHeader.rename(columns={'Trans id':'trans_id','Member id':'member_id','Store id':'store_id','Date':'date'},inplace=True)
transDetails.rename(columns={'Trans id':'trans_id','Product id':'product_id','Qty':'qty','Amount':'amount'},inplace=True)
#df=transHeader.join(transDetails,on='date',how='inner')

#df['totalsale']=df['amount'].sum().groupby()


# extract total sell per member
sellDetail = pd.merge(transHeader,transDetails,on='trans_id',how='inner')
sellDetail = sellDetail.filter(['trans_id','member_id','product_id','amount'])
sellPerMember = {}

for i in range(0,sellDetail.trans_id.count()):
    member = sellDetail['member_id'].iloc[i]
    #print(type(member))
    if(member not in sellPerMember):
        sellPerMember[member]=sellDetail['amount'].iloc[i]
    else:
        sellPerMember[member]+=sellDetail['amount'].iloc[i]
print(sellPerMember)
sellPerMemberList = []
for idx,val in sellPerMember.items():
    sellPerMemberList.append([idx,val])
totalSellPerMember=pd.DataFrame(sellPerMemberList,columns=['id','amount'])
print(totalSellPerMember)






