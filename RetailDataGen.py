from datetime import (time,datetime,timedelta)
import pandas as pd
import random

tran_hdrCol=['tran_id','member_id','store_id','purch_date']
def tran_hdr_daily(currDate,memberList):
    memberNo=random.randint(5,15)
    dataList=[]
    for idx in range(memberNo):
        member=random.choice(memberList)
        timestamp = datetime.combine(currDate,
                                 time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59)))
        tran_id = timestamp.strftime("%d-%m-%Y-%H-%M-%S")+'-'+str(member)
        line = [tran_id,member,random.randint(1, 3),timestamp.date()]
        dataList.append(line)
    return dataList

def tran_hdr(beginingDate,endDate,memberList):
    tran_hdrList=[]
    while(beginingDate<endDate):
        dailyTranHdr = tran_hdr_daily(beginingDate,memberList)
        for line in dailyTranHdr:
            tran_hdrList.append(line)
        beginingDate+=timedelta(days=1)
    return pd.DataFrame(tran_hdrList,columns=tran_hdrCol)


def tran_dtl_perTran(tran_id,currDate,productFrame):
    dataList=[]
    productNo=random.randint(1,10)
    productList=productFrame['product_id'].tolist()
    for idx in range(productNo):
        product=random.choice(productList)
        qty=random.randint(1,10)
        price=qty*productFrame['price'].loc[productFrame['product_id']==product].values[0]
        line=[tran_id,product,qty,price,currDate]
        dataList.append(line)
    return dataList

def tran_dtl(trans_idDateList,productFrame):
    tran_dtlList=[]
    for line in trans_idDateList:
        dailyTranDtl=tran_dtl_perTran(line[0],line[1],productFrame)
        for line in dailyTranDtl:
            tran_dtlList.append(line)
    return pd.DataFrame(tran_dtlList,columns=['tran_id','product_id','qty','price','purch_date'])

