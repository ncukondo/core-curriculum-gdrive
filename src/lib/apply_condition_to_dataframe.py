"""
apply condition to dataframe
"""
import re
import pandas as pd

def apply_condition_to_dataframe(data:pd.DataFrame,condition_text:str)->pd.DataFrame:
    """apply condition to dataframe"""
    conditions =re.split(r" *, *",condition_text) if isinstance(condition_text,str)  else []
    result = data.copy()
    for condition in conditions:
        unit = r" *(.+?) *"
        spliter =r" *(=|<>) *"
        pattern = f"{unit}{spliter}{unit}$"
        if reg_match:=re.match(pattern,condition):
            key,cond_type,value = reg_match.groups()
        else:
            key = condition
            cond_type = "exits"
        match cond_type:
            case "=":
                result = result.loc[result[key]==value,:]
            case "<>":
                result = result.loc[result[key]!=value,:]
            case "exits":
                result = result.loc[~result[key].isna(),:]
    return result
