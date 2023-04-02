import pandas as pd
def getEmptyCells(data_frame,column_name):
    nans = pd.isna(df[column_name])
    print(nans)
    nan_indices = []
    index_counter = 0
    for nan in nans:
        if nan == True:
            nan_indices.append(index_counter)
        index_counter = index_counter + 1
    return nan_indices

df = pd.read_csv('Sale-Items.csv')
df.drop(columns=['Register'])

#fixing empty scan code cells
nan_scan_code = getEmptyCells(df,'Scan Code')
for i in nan_scan_code:
    if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
        df.loc[df.index[i], 'Scan Code'] = '2235'
    elif df['Department'][i] == 'LOTTO ONLINE':
        df.loc[df.index[i], 'Scan Code'] = '2236'
    elif df['Department'][i] == 'LOTTO P/O':
        df.loc[df.index[i], 'Scan Code'] = '2237'

#fixing 0 values in POS cost
zero_cost = df[df['POS Cost'] == 0].index
for i in zero_cost:
    if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.2 * df['POS Retail'][i]) # mean profit is 20%. Consulted with owner. Mean used because actual gas price were not recorded by the owner
    elif df['Department'][i] == 'LOTTO ONLINE' or df['Department'][i] == 'LOTTO SCRATCH OFF':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.05 * df['POS Retail'][i]) # mean profit is 5%. Consulted with owner. Mean used because actual gas price were not recorded by the owner
    elif df['Department'][i] == 'CBD' or df['Department'][i] == 'NOVELTY' or df['Department'][i] == 'ECigs' or df['Department'][i] == 'Kratoms' :
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.45 * df['POS Retail'][i])
    elif df['Department'][i] == 'SODA' or df['Department'][i] == 'CANDY' or df['Department'][i] == 'SNACKS' or df['Department'][i] == 'TAXABLE GROCER':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.40 * df['POS Retail'][i])
    elif df['Department'][i] == 'TOBACCO' or df['Department'][i] == 'Cigarettes' or df['Department'][i] == 'MARLBORO'or df['Department'][i] == 'CIGARET CT':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.10 * df['POS Retail'][i])
    elif df['Department'][i] == 'CIG CHEAP':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.15 * df['POS Retail'][i])

    elif df['Department'][i] == 'BEER' or df['Department'][i] == 'WINE' or df['Department'][i] == 'Cigar':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.29 * df['POS Retail'][i])
    elif df['Department'][i] == 'IMP CIGAR' or df['Department'][i] == 'ICE BAG':
        df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.40 * df['POS Retail'][i])
    elif df['Department'][i] == 'NON TAX':
        df.drop(index=[i],axis=0,inplace=False)

print("Before: Size:",zero_cost.size)    
for i in range(0,10):
    print(zero_cost[i])
zero_cost = df[df['POS Cost'] == 0].index
print("After: Size:",zero_cost.size)
for i in range(0,100):
    print(df['Department'][zero_cost[i]])
df.to_csv('market_basket.csv')

