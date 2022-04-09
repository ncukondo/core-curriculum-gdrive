#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re
import os
import pandas as pd
from lib.utils import BASE_DIR,SHEETS_DIR,OUTPUT_DIR,TABLE_SOURCE_DIR,TABLE_FORMATTED_DIR
from lib.apply_condition_to_dataframe  import apply_condition_to_dataframe

df = pd.read_csv(f"{SHEETS_DIR}/別表一覧/別表一覧.csv",encoding="utf_8_sig")
df.to_csv(f"{OUTPUT_DIR}/table_index.csv",encoding="utf_8_sig",index=False)
print(f"output... table_index.csv")



os.makedirs(TABLE_FORMATTED_DIR,exist_ok=True)
for row in df.itertuples():
    source = pd.read_csv(f"{TABLE_SOURCE_DIR}/{row.データ元}.csv")
    source = apply_condition_to_dataframe(source,row.条件)
    source["id"]=source.reset_index().index+1
    source["id"]=f"TBL-{row.id}-"+source["id"].astype(str).str.zfill(3)
    source = source.loc[:,[*re.split(r" *, *",row.列),"id","UID","H28対応項目"] ]
    source.to_csv(f"{TABLE_FORMATTED_DIR}/{row.id}.csv",index=False)


# In[ ]:


import csv
import os
import pandas as pd
import re
from typing import Union, Callable
from lib.utils import BASE_DIR,SHEETS_DIR,OUTPUT_DIR
from lib.dataframe_to_grouped_numbers import dataframe_to_grouped_numbers

table_index = pd.read_csv(f"{OUTPUT_DIR}/table_index.csv",encoding="utf_8_sig")
r4_l1=pd.read_csv(f"{SHEETS_DIR}/第1層/第1層.csv")

os.makedirs(f"{OUTPUT_DIR}",exist_ok=True)

r4_l1.to_csv(f"{OUTPUT_DIR}/outcomes_l1.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./output/outcomes_l1.csv")

columns=["第1層","第2層","第2層説明","第3層","第4層","メモ","UID","H28対応項目"]
r4_l234 = pd.DataFrame(data=[],columns=columns)
r4_l2 =  pd.DataFrame(data=[],columns=[])
tabs=r4_l1["タブ名"]
for index, row in r4_l1.iterrows():
    r4_l34_unit=pd.read_csv(f"{SHEETS_DIR}/{row.タブ名}編集用/第2から4層.csv")
    r4_l2_unit=pd.read_csv(f"{SHEETS_DIR}/{row.タブ名}編集用/第2層.csv")
    r4_l2 = pd.concat([r4_l2,r4_l2_unit])
    r4_l34_unit["第1層"] = row.第1層
    r4_l34_unit = pd.merge(r4_l34_unit,r4_l2_unit,how="left",on="第2層")
    r4_l234=pd.concat([r4_l234,r4_l34_unit.loc[:,columns]])

r4_l2.to_csv(f"{OUTPUT_DIR}/outcomes_l2.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... ./output/outcomes_l2.csv")



r4=pd.merge(r4_l1,r4_l234,how="outer",on="第1層")
layers = ["第1層","第2層","第3層","第4層"]
r4=r4.dropna(subset=layers).reset_index()
nums=dataframe_to_grouped_numbers(r4,layers)
r4["id"]=r4["第1層イニシャル"]+    "-"+nums["第2層"].astype('str').str.zfill(2)+    "-"+nums["第3層"].astype('str').str.zfill(2)+    "-"+nums["第4層"].astype('str').str.zfill(2)

def format_table_ref(x:str)->str:
    def name_to_label(name:str):
        try:
            return table_index.set_index("表名").at[name,"id"]
        except KeyError:
            return ""

    def replace_func(reg:re.match)->str:
        name = reg.group(1)
        whole = reg.group(0)
        label = name_to_label(name)
        if label:
            return f"[@tbl:{label}]"
        else:
            return whole
    return re.sub(r"表\[([^\]]+)\]",replace_func,x)


r4["第4層"] = r4["第4層"].map(format_table_ref)


r4=r4.loc[:,["第1層イニシャル","第1層","第2層","第3層","第4層","id","UID","H28対応項目"]]

r4.to_csv(f"{OUTPUT_DIR}/outcomes.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print("output... outcomes.csv")

r4


# In[ ]:


import pandas as pd
import glob
import re
import csv
import os
from lib.utils import BASE_DIR,SHEETS_DIR,TABLE_SOURCE_DIR

os.makedirs( f"{TABLE_SOURCE_DIR}", exist_ok=True)
file_list = glob.glob(f"{SHEETS_DIR}/*編集用/別表-*.csv")
for file in file_list:
    name = re.search(r"別表\-(.+)\.csv",file).group(1)
    df = pd.read_csv(file,encoding="utf_8_sig")
    df.to_csv(f"{TABLE_SOURCE_DIR}/{name}.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
    print(f"output... {TABLE_SOURCE_DIR}/{name}.csv")


# In[ ]:


import pandas as pd
import glob
import re
import csv
import os
from lib.utils import BASE_DIR,SHEETS_DIR,OUTPUT_DIR


r4_l1=pd.read_csv(f"{SHEETS_DIR}/第1層/第1層.csv").loc[:,["タブ名","第1層"]]
os.makedirs(f"{OUTPUT_DIR}/tables", exist_ok=True)
file_list = glob.glob(f"{SHEETS_DIR}/*編集用/行き先がないID.csv")
df = pd.DataFrame([],columns=[])
for file in file_list:
    name = re.search(r"([^\\\/]+)編集用",file).group(1)
    unit = pd.read_csv(file,encoding="utf_8_sig")
    print(name)
    unit["タブ名"]=name
    df= pd.concat([df,unit])

df=pd.merge(df,r4_l1,how="left",on="タブ名")
df.to_csv(f"{OUTPUT_DIR}/deleted_or_moved.csv",encoding="utf_8_sig",quoting=csv.QUOTE_NONNUMERIC,index=False)
print(f"output... ./output/deleted_or_moved.csv")


# In[ ]:


import pandas as pd
import re
import os
from lib.utils import BASE_DIR,SHEETS_DIR,OUTPUT_DIR

raw=pd.read_csv(f"{SHEETS_DIR}/H28/H28.csv", index_col=0)
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

distdir=f"{OUTPUT_DIR}/2016"
os.makedirs(distdir,exist_ok=True)
data.to_csv(f"{distdir}/goals.csv", encoding = "utf_8_sig", index=False)
data

