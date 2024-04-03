import csv
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="{dDO`HklZa!@|]xoV[r&",
    database="retail_pro"
)
path=r'/home/kiran/code/RetailProject/'
tran_hdrPath = f"{path}tran_hdr.csv"
tran_dtlPath = f"{path}tran_dtl.csv"
cursor = mydb.cursor()

with open(tran_hdrPath) as fs:
    data=csv.reader(fs)
    next(data)
    for row in data:
        cursor.execute('INSERT INTO trans_hdr VALUES(%s,%s,%s,%s)',row)
        
with open(tran_dtlPath) as fs:
    data=csv.reader(fs)
    next(data)
    for row in data:
        cursor.execute('''INSERT INTO trans_dtl(trans_id,product_id,qty,amount,trans_date) VALUES(%s,%s,%s,%s,%s) 
        ON DUPLICATE KEY UPDATE qty=VALUES(qty),amount=VALUES(amount),trans_date=VALUES(trans_date)''',row)

'''
cursor.execute('TRUNCATE TABLE trans_hdr')

'''
mydb.commit()
cursor.close()
mydb.close()

