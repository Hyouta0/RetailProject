import csv
import mysql.connector

DotPath='/home/kiran/code/RetailProject/Data/.retail'
tranPaths=[]
with open(DotPath) as dot:
    for line in dot:
        tranPaths.append(line.strip().split(','))
with open(DotPath,'w') as dot:
    dot.truncate()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="{dDO`HklZa!@|]xoV[r&",
    database="retail_pro"
)
cursor = mydb.cursor()
for tranPath in tranPaths:
    with open(tranPath[0]) as fs:
        data = csv.reader(fs)
        next(data)
        for row in data:
            cursor.execute('INSERT INTO trans_hdr VALUES(%s,%s,%s,%s)', row)

    with open(tranPath[1]) as fs:
        data = csv.reader(fs)
        next(data)
        for row in data:
            cursor.execute('''INSERT INTO trans_dtl(trans_id,product_id,qty,amount,trans_date) VALUES(%s,%s,%s,%s,%s) 
            ON DUPLICATE KEY UPDATE qty=VALUES(qty),amount=VALUES(amount)''', row)

mydb.commit()
cursor.close()
mydb.close()

print("Done")