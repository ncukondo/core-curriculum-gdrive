#!/usr/bin/env python
# coding: utf-8

# In[10]:


import csv
import os
import pandas as pd

r4_l1=pd.read_csv("./sheets/第1層/第1層.csv")

os.makedirs("./output",exist_ok=True)

r4_l1.to_csv("./output/outcomes_l1.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./output/outcomes_l1.csv")

columns=["第1層","第2層","第2層説明","第3層","第4層","メモ","UID","H28対応項目"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
r4_l2 =  pd.DataFrame(data=[],columns=[])
tabs=r4_l1["タブ名"]
for index, row in r4_l1.iterrows():
    r4_l34_unit=pd.read_csv(f"./sheets/{row.タブ名}編集用/第2から4層.csv")
    r4_l2_unit=pd.read_csv(f"./sheets/{row.タブ名}編集用/第2層.csv")
    r4_l2 = pd.concat([r4_l2,r4_l2_unit])
    r4_l34_unit["第1層"] = row.第1層
    r4_l34_unit = pd.merge(r4_l34_unit,r4_l2_unit,how="left",on="第2層")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l2.to_csv("./output/outcomes_l2.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./output/outcomes_l2.csv")

r4_full=pd.merge(r4_l1,r4_l234,how="outer",on="第1層")
r4_full=r4_full.dropna(subset=["第1層","第2層","第3層","第4層"])
r4_full.loc[:,["第1層","第2層","第3層","第4層","UID","H28対応項目"]].to_csv("./output/outcomes.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... outcomes.csv")

r4_full


# In[11]:


import pandas as pd
import glob
import re
import csv
import os

os.makedirs( "output/tables", exist_ok=True)
file_list = glob.glob(f"./sheets/*編集用/別表-*.csv")
for file in file_list:
    name = re.search(r"別表\-(.+)\.csv",file).group(1)
    df = pd.read_csv(file,encoding="utf_8_sig")
    df.to_csv(f"./output/tables/{name}.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
    print(f"output... ./output/tables/{name}.csv")


# In[12]:


import pandas as pd
import glob
import re
import csv
import os

r4_l1=pd.read_csv("./sheets/第1層/第1層.csv").loc[:,["タブ名","第1層"]]
os.makedirs("output/tables", exist_ok=True)
file_list = glob.glob(f"./sheets/*編集用/行き先がないID.csv")
df = pd.DataFrame([],columns=[])
for file in file_list:
    name = re.search(r"([^\\\/]+)編集用",file).group(1)
    unit = pd.read_csv(file,encoding="utf_8_sig")
    print(name)
    unit["タブ名"]=name
    df= pd.concat([df,unit])

df=pd.merge(df,r4_l1,how="left",on="タブ名")
df.to_csv(f"./output/deleted_or_moved.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print(f"output... ./output/deleted_or_moved.csv")


# In[13]:


import pandas as pd
import re
import os

raw=pd.read_csv("./sheets/H28/H28.csv", index_col=0)
raw


data=pd.DataFrame([])
data["id1"]=raw["第1層（大項目）"].str.extract(r"^(.)")
data["text1"]=raw["第1層（大項目）"].str.extract(r"^. ?(.+)")
data["id2"]=raw["第2層（中項目）"].str.extract(r"^.\-(\d+)")
data["id2"]=data["id1"]+"-"+data["id2"].str.zfill(2)
data["text2"]=raw["第2層（中項目）"].str.extract(r"^.\-\d+ (.+)")
data["id3"]=raw["第3層（小項目）"].str.extract(r"^.\-\d+\-(\d+)")
data["id3"]=data["id2"]+"-"+data["id3"].str.zfill(2)
data["text3"]=raw["第3層（小項目）"].str.extract(r"^.\-\d+\-\d+\) (.+)")
raw["id3"]=data["id3"]

id4_list=[]
text4_list=[]
current_parent=""
prev_text=""
current_index=0
for index,row in raw.iterrows():
  text=row["第4層（細小項目）"]
  parent=row["id3"]
  if parent!= current_parent:
    current_index=0
    prev_text=""
  if prev_text!= text:
    current_index=current_index+1
  current_parent=parent
  prev_text=text
  if text=="なし":
    id4_list.append(f"{parent}-na")
    text4_list.append(text)
  else:
    id4_list.append(f"{parent}-{str(current_index).zfill(2)}")
    text4_list.append(re.sub(r"^.\-\d+\-\d+\)\-\(\d+\) ","",str(text)))

data["id4"]=id4_list
data["text4"]=text4_list
raw["id4"]=data["id4"]

id5_list=[]
text5_list=[]
current_parent=""
prev_text=""
current_index=0
for index,row in raw.iterrows():
  text=row["第5層（学修目標）"]
  parent=row["id4"]
  if parent!= current_parent:
    current_index=0
    prev_text=""
  if prev_text!= text:
    current_index=current_index+1
  current_parent=parent
  prev_text=text
  if text=="なし":
    id5_list.append(f"{parent}-na")
    text5_list.append(text)
  else:
    id5_list.append(f"{parent}-{str(current_index).zfill(2)}")
    item_text=re.sub(r"^([.０-９0-9]{1,2})( |\.|．)","",str(text))
    item_text=re.sub(r"^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖]","",str(item_text))
    text5_list.append(item_text)

data["id5"]=id5_list
data["text5"]=text5_list

distdir="./output/2016/"
os.makedirs(distdir,exist_ok=True)
data.to_csv(f"{distdir}H28.csv",encoding="utf_8_sig")
data

