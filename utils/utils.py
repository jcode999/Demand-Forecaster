import pandas as pd
from datetime import datetime
from meteostat import Point, Daily

def collect_weekly_weather_data(start,end,str_start,str_end,df_origin):
    
    
    # Create Point for location of business, BC
    frst_hll = Point(32.6721 , -97.2692, 70)
    
    # Create Point for Vancouver, BC
    data = Daily(frst_hll, start, end)
    data = data.fetch()
    #date_range = pd.date_range(start='2021-01-01', end='2022-12-31', freq='D')
    date_range = pd.date_range(start = str_start, end = str_end, freq='D')
    data['date'] = date_range

    daily = data['tavg']
    
    week = data.groupby(pd.Grouper(key="date", freq="7D",origin=df_origin)).agg({'tavg':'mean'})
    week_reset = week.reset_index()
    # Plot line chart including average, minimum and maximum temperature
    #data.plot(y=['tavg', 'tmin', 'tmax'])
    #plt.show()
    print(daily)
    return week_reset,daily

def collect_weekly_gas_avg(paths):
    for path in paths:
        week_gas_df = pd.read_csv(path)
    return week_gas_df

def getEmptyCells(data_frame,column_name):
    nans = pd.isna(data_frame[column_name])
    nan_indices = []
    index_counter = 0
    for nan in nans:
        if nan == True:
            nan_indices.append(index_counter)
        index_counter = index_counter + 1
    return nan_indices

def check_for_holiday(holiday_dates,week_start,week_end):
    #Converting the date to pandas datetime
    for holiday_date in holiday_dates:
        date_pd = pd.to_datetime(holiday_date)
        #Converting the week start and end to pandas datetime
        week_start_pd = pd.to_datetime(week_start)
        week_end_pd = pd.to_datetime(week_end)

        #Checking if the date falls in the given week
        if date_pd >= week_start_pd and date_pd <= week_end_pd:
            return 1
        else:
            return 0
    
def econimic_indicators():
    import requests
    import json
    import prettytable
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0','SUUR0000SA0'],"startyear":"2020", "endyear":"2022"})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    for series in json_data['Results']['series']:
        x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
        
            if 'M01' <= period <= 'M12':
                x.add_row([seriesId,year,period,value,footnotes[0:-1]])
        output = open(seriesId + '.txt','w')
        output.write (x.get_string())
        output.close()

def clean_up(df):
    #remove all unidentified items except for gas and lotto online
    nan_scan_code = getEmptyCells(df,'Scan Code')
    for i in nan_scan_code:
        if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
            df.loc[df.index[i], 'Scan Code'] = '2235'
            df.loc[df.index[i], 'Department'] = 'GAS'
        elif df['Department'][i] == 'LOTTO ONLINE':
            df.loc[df.index[i], 'Scan Code'] = '2236'

    print("Before removing nan scan codes : ",df.shape)
    nan_scan_code = getEmptyCells(df,'Scan Code')

    #drop NaN scan codes
    df.drop(index=nan_scan_code,axis=0,inplace=True)
    print("After removing NaN scan codes : ",df.shape)
    df.drop(columns=['Register','Unnamed: 14'],inplace=True)
    df.reset_index(inplace = True)
    df.drop(columns=['index'],inplace=True)
    
    #remove other invalid scan codes
    invalid_scan_codes = df['Scan Code'].str.match("^[0-9]*$")
    invalid_indices = [i for i, x in enumerate(invalid_scan_codes) if x==False]
    df.drop(invalid_indices,axis=0,inplace=True)
    df.reset_index(inplace = True)
    df.drop(columns=['index'],inplace=True)
    
    #remove zero pos cost
    zero_cost = df[df['POS Cost'] == 0].index
    for i in zero_cost:
        if df['Department'][i] == 'GAS PUMP #1' or df['Department'][i] == 'GAS PUMP #2' or df['Department'][i] == 'GAS PUMP #3' or df['Department'][i] == 'GAS PUMP #4':
            df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.2 * df['POS Retail'][i]) # mean profit is 20%. Consulted with owner. Mean used because actual gas price were not recorded by the owner
        elif df['Department'][i] == 'LOTTO ONLINE' or df['Department'][i] == 'LOTTO SCRATCH OFF':
            df.loc[df.index[i], 'POS Cost'] = df['POS Retail'][i] -  (0.05 * df['POS Retail'][i]) 

    zero_cost = df[df['POS Cost'] < 0].index
    df.drop(index=zero_cost,axis=0,inplace=True)
    df.reset_index(inplace = True)
    df.drop(columns=['index'],inplace=True)
    print("After removing numm zero costs : ",df.shape)
    
    #calculate discount amount to record if there was a sale on the product
    zero_retail = getEmptyCells(df,'Retail at Sale')
    df['Discounts'] = ''
    for i in zero_retail:
        df['Retail at Sale'][i] = df['POS Retail'][i]
    df['Discounts'] = df['Retail at Sale'] - df['POS Retail']
    
    #encode nominal values
    #df['Int Dept'] = pd.factorize(df['Department'])[0]
    #holiday data
    
    
    
    return df
def convert_weekly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    weekly_df = df.groupby([pd.Grouper(key="Date", freq="7D",origin='2021-01-01'),'Scan Code','Description','Department']).agg({'Qty':'sum','POS Cost':'mean','POS Retail':'mean','Discounts':'mean'})
    weekly_df.reset_index(inplace=True)
    weekly_df['Month'] = weekly_df['Date'].dt.month
    weekly_df['Week'] = weekly_df['Date'].dt.isocalendar().week
    weekly_df['Year'] = weekly_df['Date'].dt.year
    #weather data
    start = datetime(2021, 1, 1)
    end = datetime(2022, 12, 31)
    weekly_df['Avg Temp'] = ''
    weekly_avg_temp,Daily = collect_weekly_weather_data(start,end,'2021-01-01','2022-12-31','2021-01-01')
    weeks = list(weekly_avg_temp['date'])
    temps = list(weekly_avg_temp['tavg']) 
    week_counter = 0
    for i in range(0,len(weeks)):
        dates = weekly_df[weekly_df['Date'] == weeks[i]].index
        weekly_df.loc[dates, 'Avg Temp'] = temps[i]
    
    return holidays(weekly_df)

def holidays(weekly_df):
    from datetime import date
    #from utils.utils import check_for_holiday
    weekly_df['Holiday'] = 0
    holiday_df = pd.read_csv('data/csv/original/holidays_2022.csv')
    holiday_df['Dates'] = pd.to_datetime(holiday_df['Dates'])
    holiday_weekly_df = holiday_df.groupby([pd.Grouper(key="Dates", freq="7D",origin='2021-01-01')]).agg({'Value':'sum'})
    holiday_weekly_df.reset_index(inplace = True)
    holiday_dates = holiday_weekly_df['Dates']
    holiday_values = holiday_weekly_df['Value']
    for i in range(0,len(holiday_weekly_df)):
        weekly_df.loc[(weekly_df['Date'].dt.isocalendar().week == holiday_dates[i].week),'Holiday'] = holiday_values[i]
    return weekly_df

def get_2023_test():
    df = pd.read_csv('data/csv/original/sales2023.csv',dtype={'Scan Code':str})
    df = clean_up(df)
    weekly_df = convert_weekly(df)
    return weekly_df


def product_info(product_code):
    import urllib.request
    import json
    import pprint

    from urllib.request import Request, urlopen

    api_key = 'e121bfe8d7be3c72448b3fd0d99ce7b9c8a9278051c80a8a9a468a2abd494e15'

    req = Request('https://go-upc.com/api/v1/code/' + product_code)
    req.add_header('Authorization', 'Bearer ' + api_key)

    content = urlopen(req).read()
    data = json.loads(content.decode())

    product_name = data["product"]["name"]
    product_description = data["product"]["description"]
    product_image = data["product"]["imageUrl"]

    # print("Product Name: " + product_name + "\n")
    # print("Product Description: " + product_description + "\n")
    # print("Product Image URL: " + product_image + "\n")

    print(data)
    print('-----------------------------------------------------------')

start = datetime(2021, 1, 1)
end = datetime(2022, 12, 31)
week,day = collect_weekly_weather_data(start,end,'2021-01-01','2022-12-31','2021-01-01')
print(day)

