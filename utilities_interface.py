import UtilsProject as up
import pandas as pd
 
def convert_xlsx(file_path):
    df = pd.read_excel(file_path, header = None)
    array = df.to_numpy()
    dict_query = {}
    for row in array:
        key = row[0]
        values_i = row[range(1,len(row))]
        values = values_i[~pd.isna(values_i)]
        dict_query[key]= values

    query = up.make_query(dict_query)
    return query

def convert_txt(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query