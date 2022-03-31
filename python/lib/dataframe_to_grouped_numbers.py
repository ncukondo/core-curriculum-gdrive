'''
get grouped numbers for dataframe
'''
import pandas as pd

def dataframe_to_grouped_numbers(data:pd.DataFrame,target_columns:list[str]):
    '''get grouped numbers for dataframe'''
    def get_numbers_for_group(sub_df:pd.DataFrame,sub_columns):
        groups = sub_df.groupby([sub_columns[0]],sort=False)
        return (groups.cumcount()==0).cumsum()

    df = data.reset_index()
    columns = target_columns.copy()
    numbers = pd.DataFrame([[0]*len(columns) for _ in range(len(df))],columns=columns)
    numbers[columns[0]]=get_numbers_for_group(df,columns)
    for i,colname in enumerate(columns[1:]):
        indexes =[group.index for _,group in df.groupby(columns[0:i+1],sort=False)]
        for index in indexes:
            sub_df= df.iloc[index,:]
            numbers.loc[index,colname]=get_numbers_for_group(sub_df,columns[i+1:])

    return numbers
