import pandas as pd

path = r'./member_data.csv'

members = pd.read_csv(path,header=None,names=["Id","Fname","Lname","store_id","Date"])

print(type(members['Id'].count()))
for i in range(0,members['Id'].count()):
    members.iloc[i,[0]]=i+1

members.to_csv('./memberData.csv',index=False)