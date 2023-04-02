import pandas as pd

def getEmptyCells(data_frame,column_name):
    nans = pd.isna(data_frame[column_name])
    nan_indices = []
    index_counter = 0
    for nan in nans:
        if nan == True:
            nan_indices.append(index_counter)
        index_counter = index_counter + 1
    return nan_indices

df = pd.read_csv('Sale-Items.csv')

#remove all unidentified items
nan_scan_code = getEmptyCells(df,'Scan Code')
for i in nan_scan_code:
    if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
        df.loc[df.index[i], 'Scan Code'] = '2235'
    elif df['Department'][i] == 'LOTTO ONLINE':
        df.loc[df.index[i], 'Scan Code'] = '2236'
print("Before removing numm scan codes : ",df.shape)

nan_scan_code = getEmptyCells(df,'Scan Code')
df.drop(index=nan_scan_code,axis=0,inplace=True)
print("After removing numm scan codes : ",df.shape)
df.drop(columns=['Register','Unnamed: 14'],inplace=True)
df.to_csv('demand_forecast.csv',index=False,index_label=False)

df = pd.read_csv('demand_forecast.csv',low_memory=False)
zero_cost = df[df['POS Cost'] == 0].index
for i in zero_cost:
    if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.2 * df['POS Retail'][i]) # mean profit is 20%. Consulted with owner. Mean used because actual gas price were not recorded by the owner
    elif df['Department'][i] == 'LOTTO ONLINE' or df['Department'][i] == 'LOTTO SCRATCH OFF':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.05 * df['POS Retail'][i]) 

zero_cost = df[df['POS Cost'] == 0].index
df.drop(index=zero_cost,axis=0,inplace=True)
print("After removing numm zero costs : ",df.shape)
print(df['Date'].min() , df['Date'].max())
df['Date'] = pd.to_datetime(df['Date'])


# df.index = pd.to_datetime(df.index)
# print(df.index)
# # dfn = df.set_index('Date').resample('1H').pad()
# # print(dfn)
df.to_csv('demand_forecast.csv')





