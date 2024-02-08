from datetime import (date as Date, time as Time,timedelta as TimeDelta)
import pandas as pd
import random
#import os
#import shutil as sh

#paths
membersPath = r'./member_data.csv'
productsPath = r'./product.csv'

#dataframe
members = pd.read_csv(membersPath,header=None ,names=['member_id','f_name','l_name','store_id','member_date'])
products = pd.read_csv(productsPath)

#data
startDate = Date(2021,1,1)
endDate =Date.today()
membersIdList = members['member_id'].to_list()
productsIdList = products['product_id'].to_list()
transHeaderList = []
transDetailList = []
productPrices = {}

#product prict data extration
cnt = -1
for line in open(productsPath):
    if(cnt == -1):
        cnt +=1
        continue
    id,desc,price,cat,qry=line.strip().split(",")
    id = int(id)
    price = float(price)
    if id not in productPrices:
        productPrices[id]=price

#retail

while(startDate<=endDate):
    totalMembers =random.randint(15,40)
    visitedMembers = random.choices(membersIdList,k=totalMembers)
    for member in visitedMembers:
        storeId = random.randint(1,3)
        totalProduct = random.randint(1,10)
        boughtProducts = random.choices(productsIdList,k=totalProduct)
        transId = startDate.strftime("%d-%m-%Y")+"_" \
                +str(Time(random.randint(1,23),random.randint(1,59),random.randint(1,59)))+ \
                "_"+str(member)+"_"+str(storeId)
        for product in boughtProducts:
            qty =random.randint(1,5)
            transHeaderTmpList = [transId,member,storeId,startDate]
            transDetailTmpList = [transId,product,qty,(qty*productPrices[product]),startDate]
            transHeaderList.append(transHeaderTmpList)
            transDetailList.append(transDetailTmpList)
    startDate+=TimeDelta(days=1)


#create new dataFrame
transHeader = pd.DataFrame(transHeaderList,columns=["trans_id","member_id","store_id","trans_date"])
transHeader=transHeader.drop_duplicates()
transDetail = pd.DataFrame(transDetailList,columns=["trans_id","product_id","qty","amount","trans_date"])

#writing to csv
transHeader.to_csv(r'./transHeader.csv',index=False)
transDetail.to_csv(r'./transDetail.csv',index=False)