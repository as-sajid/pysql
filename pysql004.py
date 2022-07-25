import json
from urllib import request
url = "https://production.api.coindesk.com/v2/tb/price/ticker?assets=all"
response = request.urlopen(url)
data = json.loads(response.read().decode())
#print(data)
''''Flatten the JSON '''
def flatten_json(coin_dict):
    flatten_dict = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for key in x:
                flatten(x[key], name + key + '_')
        else:
            flatten_dict[name[:-1]] = x
    flatten(coin_dict)
    return flatten_dict
import pandas as pd
master_df = pd.DataFrame()
for coin in data['data'].keys():
    temp_df = pd.json_normalize(flatten_json(data['data'][coin]))
    frames=[master_df,temp_df]
    master_df=pd.concat(frames)
    #master_df = master_df.append(temp_df)
print(master_df.head(5))
master_df = master_df[['iso', 'name', 'ohlc_o', 'ohlc_h', 'ohlc_l', 'ohlc_c', 'change_percent']].reset_index(drop=True)
master_df.columns = ['Symbol', 'Name', 'Open', 'High', 'Low', 'Close', 'Pct_Change']
master_df.iloc[:, 2:] = master_df.iloc[:, 2:].apply(lambda x: round(x, 2))
master_df['Pct_Change'] = (master_df['Pct_Change'] / 100).round(2)
master_df = master_df.sort_values('Pct_Change', ascending=False).reset_index(drop=True)
print(master_df.head(11))
master_df.to_csv('master_df.csv', index=False)
file_name = "Cryptocurrency.xlsx"
sheet_name = "Summary"
import xlsxwriter
writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
master_df.to_excel(writer, sheet_name=sheet_name, startrow = 2, index = False)