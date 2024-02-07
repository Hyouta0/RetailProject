import datetime
from datetime import (
datetime as DateTime,
date     as  Date,
time     as Time,
timedelta as TimeDelta
)
import random
import pandas as pd


#data
path= r"./retail.csv"
productPath = r"./product.csv"
headerLine = "Date,Trans_id,Member_id,Store_id,Product_id,Qty,Total_Price\n"

startDate = Date(2021,1,1)
endDate =Date.today()

idList = []
for i in range(1,101):
    idList.append(i)
productPrice={}

#product prict data extration
cnt = -1
for line in open(productPath):
    if(cnt == -1):
        cnt +=1
        continue
    id,desc,price,cat,qry=line.strip().split(",")
    id = int(id)
    price = float(price)
    if id not in productPrice:
        productPrice[id]=price

#retail csv
fp = open(path,'a')
fp.write(headerLine)

while(startDate<=endDate):
    totalMember = random.randint(15,40)
    members = random.choices(idList,k=totalMember)
    for member in members:
        storeid = random.randint(1,3)
        totalProduct = random.randint(1,10)
        products = random.choices(idList,k=totalProduct)
        trans = startDate.strftime("%d-%m-%Y")+"_"\
                +str(Time(random.randint(1,23),random.randint(1,59),random.randint(1,59)))+\
            "_"+str(member)+"_"+str(storeid)
        for product in products:
            qty = random.randint(1,5)
            line=startDate.strftime("%d-%m-%Y")\
                 +","+trans\
                 +","+str(member)+","\
                 +str(storeid)+","\
                 +str(product)+","\
                 +str(qty)+","\
                 +str(productPrice[product]*qty)+"\n"
            fp.write(line)
            print(line,end="")
    startDate+=TimeDelta(days=1)


fp.close()
