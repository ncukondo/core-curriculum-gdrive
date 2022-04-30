import os
import json
import tempfile

from dateutil.parser import parse as parse_date

from lib.google_drive import from_service_account


def export_google_sheets(folder_dict:dict[str,str],dist_dir:str=None,info_store_file:str=""):
    """ export excel from google sheet"""
    epoc_time='1970-01-01T00:00:00.000+00:00'

    if dist_dir is None:
        dist_dir=os.path.join(tempfile.gettempdir(),"exported_excel")
    os.makedirs(dist_dir, exist_ok=True)

    drive = from_service_account()
    gsheets_info={}
    try:
        if len(info_store_file)>0:
            with open(info_store_file,"r",encoding="utf_8") as f:
                gsheets_info=json.load(f)
    except:
        print(f"file not found({info_store_file})")

    global_updated=gsheets_info.get("global",{}).get("updated",epoc_time)
    query="\n and \n".join([ 
        "mimeType='application/vnd.google-apps.spreadsheet'",
        f"modifiedTime > '{global_updated}'",
        "trashed=false",
        f"""({" or ".join([f"'{x}' in parents" for x in folder_dict.values()])})"""
    ])
    try:
        file_list =drive.get_list(query,["name","id","modifiedTime","parents"])
        for file in file_list:
            timestamp=file["modifiedTime"]
            file["timestamp"]=timestamp
            last_recorded_time=gsheets_info\
                .get("files",{}).get(file["id"],{})\
                .get("timestamp",epoc_time)
            if parse_date(timestamp) <= parse_date(last_recorded_time):
                print(f"skip: {file['name']}")
                continue

            dir_name = dist_dir
            for key,folder_id in folder_dict.items():
                if folder_id in file["parents"]:
                    dir_name = os.path.join(dist_dir,key)
            os.makedirs(dir_name,exist_ok=True)
            file["export_path"]=drive.export(file["id"],"xlsx",dir_name)
            yield file

            print(f'{file["name"]} in {timestamp}')
            gsheets_info["files"]=gsheets_info.get("files",{})
            gsheets_info["files"][file["id"]]={"timestamp":timestamp,"name":file["name"],"id":file["id"]}
            if parse_date(global_updated) < parse_date(file["modifiedTime"]):
                global_updated=file["modifiedTime"]

        gsheets_info["global"]=gsheets_info.get("global",{})
        gsheets_info["global"]["updated"]=global_updated
    except:
        raise
    finally:
        if len(info_store_file)>0:
            with open(info_store_file,"w",encoding="utf_8") as f:
                json.dump(gsheets_info,f,indent=4, ensure_ascii=False)
