import pandas as pd
import numpy as np
import csv


csvfile = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/After_price_change/CVX.csv'
real_cvx_price = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/Real_prices_Alpha_vantage/daily_CVX.csv'

df = pd.read_csv(csvfile)
df['stock'] = 'CVX'

df['price_target'].replace('', np.nan, inplace=True)
df.dropna(subset=['price_target'], inplace=True)
df[['Month','Day','Year']] = df['date'].str.split('/',expand=True)
df['timestamp'] = pd.to_datetime(arg=df[['Day', 'Month', 'Year']],format='%d/%m/%Y')
# df['timestamp'] = df['Year'] + '-' + df['Day'] + '-' + df['Month']
df.drop(df.columns[0], axis=1, inplace=True)
# df.reindex(columns=['Year','Month','Date','stock','Brokerage','price_target']‌​).to_csv('csvfile.csv', index=False,header=False)
# df.reindex(columns=['Year','Month','Day','stock','brokerage','price_target'])
# df.drop(df.columns[[3,4]], axis=1, inplace=True)
# df.to_csv(csvfile)
# df.to_numeric(df[['Year','Month','Day']])
df.apply(pd.to_numeric, errors='ignore')
df.sort_values('timestamp')

df1 = pd.read_csv(real_cvx_price)
# df1.drop(df1.columns[[2,3,4,5]], axis=1, inplace=True)
df1[['Year','Month','Day']] = df1['timestamp'].str.split('-', expand=True)
# df1.to_csv(real_apple_price)
# df1['Day'] = df1[['Year','Month','Day']].str.strip()
# df.to_numeric(df[['Year','Month','Day']])
pd.options.mode.chained_assignment = None  # default='warn'
for i in range(len(df1['Month'])):
    if df1['Month'][i][0] == '0':
        a = df1['Month'][i][1:]
        df1['Month'][i] = a
    if df1['Day'][i][0] == '0':
         df1['Day'][i] = df1['Day'][i][1:]
df1.apply(pd.to_numeric, errors='ignore')
df1['timestamp'] = pd.to_datetime(arg=df1[['Day', 'Month', 'Year']],format='%d/%m/%Y')
df1.sort_values('timestamp')

# joined = pd.merge(df,df1, how='left', left_on=['Year','Month','Day'] , right_on=['Year','Month','Day'])
joined = pd.merge(df, df1, how='left', on=['Year', 'Month', 'Day'])
# joined = pd.merge_asof(df.sort_values('timestamp'), df1.sort_values('timestamp'), on='timestamp', by='timestamp')
joined_path = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/New_lists/CVX.csv'

joined.dropna(subset=['open'], inplace=True)

joined['yield'] = joined['price_target']/joined['open'] - 1
joined = joined[['Year','Month','Day','stock','brokerage','yield','price_target', 'open']]
joined.to_csv(joined_path)

