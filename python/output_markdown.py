#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re
from lib.utils import BASE_DIR,SHEETS_DIR,OUTPUT_DIR

from lib.dataframe_to_text import dataframe_to_text


r4=pd.read_csv(f"{OUTPUT_DIR}/outcomes.csv")
r4_l1=pd.read_csv(f"{OUTPUT_DIR}/outcomes_l1.csv")
r4_l2=pd.read_csv(f"{OUTPUT_DIR}/outcomes_l2.csv")
r4=pd.merge(r4_l2,r4,how="right",on="第2層")
r4=pd.merge(r4_l1,r4,how="right",on="第1層")
r4=r4.dropna(subset=["第1層","第2層","第3層","第4層"]).fillna("")

r4_to_md_draft=pd.DataFrame(data=[],columns=["第1層","第2層","第3層","第4層"])
r4_to_md_draft["第1層"]="\n"+"# "+r4["第1層"]+"\n\n"+r4["第1層説明"]+"\n"
r4_to_md_draft["第2層"]="\n"+"## "+r4["第2層"]+"\n\n"+r4["第2層説明"]+"\n"
r4_to_md_draft["第3層"]="\n"+"### "+r4["第3層"]+"\n"
r4_to_md_draft["第4層"]="1. "+r4["第4層"]
r4_to_md_draft=r4_to_md_draft.dropna(subset=["第1層","第2層","第3層","第4層"])

r4_md_draft = dataframe_to_text(r4_to_md_draft)

with open(f"{OUTPUT_DIR}/outcomes.md","w") as f:
    f.write(r4_md_draft)
print("output... ./dist/outcomes.md")

