import os
import tempfile

from dateutil.parser import parse as parse_date

from lib.google_drive import from_service_account


def export_google_docs(folder_dict:dict[str,str],dist_dir:str=None):

    if dist_dir is None:
        dist_dir=os.path.join(tempfile.gettempdir(),"exported_docx")
    os.makedirs(dist_dir, exist_ok=True)

    drive = from_service_account()
    query="\n and \n".join([ 
        "mimeType='application/vnd.google-apps.document'",
        "trashed=false",
        f"""({" or ".join([f"'{x}' in parents" for x in folder_dict.values()])})"""
    ])
    try:
        file_list =drive.get_list(query,["name","id","modifiedTime","parents"])
        for file in file_list:
            timestamp=file["modifiedTime"]
            file["timestamp"]=timestamp

            dir_name = dist_dir
            for key,folder_id in folder_dict.items():
                if folder_id in file["parents"]:
                    dir_name = os.path.join(dist_dir,key)
            os.makedirs(dir_name,exist_ok=True)
            file["export_path"]=drive.export(file["id"],"docx",dir_name)
            yield file

            print(f'{file["name"]} in {timestamp}')

    except:
        raise
