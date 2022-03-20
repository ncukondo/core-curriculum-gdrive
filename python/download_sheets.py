#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import tempfile
import pandas as pd
import csv
import shutil

from lib.utils import BASE_DIR
from lib.export_google_sheets import export_google_sheets


folder_ids=[
        '1IDl3cSc8u5y4Gf13_PBCEZdFFnDv6Ilz', #入力
        '1FlCwwi71s1BI4uhOf2CefX85byj1Alo_', #各チーム編集用シート
]
DIST_DIR=f"{BASE_DIR}/sheets/"
info_file = f"{DIST_DIR}sheets_info.json"

if os.path.exists(DIST_DIR) and os.path.exists(info_file):
    shutil.rmtree(DIST_DIR)

os.makedirs(DIST_DIR,exist_ok=True)

try:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_list=export_google_sheets(folder_ids,temp_dir,info_stor_file=f"{DIST_DIR}sheets_info.json")
        for file in file_list:
            book = pd.ExcelFile(file["export_path"])
            dir_name = os.path.join(DIST_DIR,file['name'])
            os.makedirs(dir_name,exist_ok=True)
            for name in book.sheet_names:
                sheet:pd.DataFrame = book.parse(name)
                sheet.to_csv(os.path.join(dir_name,f"{name}.csv"),quoting=csv.QUOTE_NONNUMERIC,encoding="utf_8_sig",index=False,)
        os.remove(info_file)
except:
    raise

