import pandas as pd
import numpy as np
import datetime
def getEmptyCells(data_frame,column_name):
    nans = pd.isna(data_frame[column_name])
    nan_indices = []
    index_counter = 0
    for nan in nans:
        if nan == True:
            nan_indices.append(index_counter)
        index_counter = index_counter + 1
    return nan_indices
d = {'code':['789','123','123','123','456'],'qty':[9,-1,2,3,1],'date':['01/11/2023','01/03/2022','01/03/2022','01/04/2022','01/09/2022']}

df = pd.DataFrame(data=d)
df['date'] = pd.to_datetime(df['date'])
df['Week Number'] = df['date'].dt.week

print(df)
grp = df.groupby([pd.Grouper(key="date", freq="1W", origin='2022-01-02'),'code']).agg({'qty':'sum'})
print(grp)

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 1, 6)
delta = end_date - start_date

date_range = []
for i in range(delta.days + 1):
    date_range.append(start_date + datetime.timedelta(i))
items = ['123',np.nan,'123','123',np.nan,'567']
department = ['Cigs','Lotto','Cigs','Cigs','Cigs','Novelty']
d = {'date':date_range,'qty':[1,1,1,1,1,6],'items':items,'Dept':department }
df = pd.DataFrame(data=d)

#dealing with nan values
nan = getEmptyCells(df,'items')
print("NAN idexes before Lotto fix: ",nan)
for i in nan:
    if df['Dept'][i] == 'Lotto':
        df.loc[df.index[i], 'items'] = '2235'

nan = getEmptyCells(df,'items')
print("NAN idexes after Lotto fix: ",nan)
df['date'] = pd.to_datetime(df['date'])
print('After fixing lotto: Frame \n',df)

df.drop(index=nan,axis=0,inplace=True)
rest = df.reset_index()
print('DF after drop:\n',df)
grp = df.groupby([pd.Grouper(key="date", freq="7D",origin='2020-01-01'),'items','Dept']).agg({'qty':'sum'})

df.drop(columns=['Dept'],inplace=True)
print(df['date'].dt.normalize())
print('*************** GRP ******************')
print(len(rest))
print(rest.drop(columns=['index']))

if rest['date'][0] == pd.to_datetime('2020-01-01'):
    print('ok')

    