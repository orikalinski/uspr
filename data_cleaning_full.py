import pandas as pd
import numpy as np
import csv

company_list = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/daw_jones_30_links.csv'

with open(company_list) as f:
    reader = csv.reader(f)
    companies = [row[0] for row in reader]


def clean(company_name):
    stock_recommends = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/After_price_change/%s.csv'
    real_price = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/Real_prices_Alpha_vantage/daily_%s.csv'
    stock = stock_recommends % company_name
    price = real_price % company_name
    df = pd.read_csv(stock)
    df['stock'] = company_name

    df['price_target'].replace('', np.nan, inplace=True)
    df.dropna(subset=['price_target'], inplace=True)
    df[['Month', 'Day', 'Year']] = df['date'].str.split('/', expand=True)
    df['timestamp'] = pd.to_datetime(arg=df[['Day', 'Month', 'Year']], format='%d/%m/%Y')
    # df['timestamp'] = df['Year'] + '-' + df['Day'] + '-' + df['Month']
    df.drop(df.columns[0], axis=1, inplace=True)
    df.apply(pd.to_numeric, errors='ignore')

    # df.to_csv(csvfile)

    df1 = pd.read_csv(price)
    df1.drop(df1.columns[[2, 3, 4, 5]], axis=1, inplace=True)
    df1[['Year', 'Month', 'Day']] = df1['timestamp'].str.split('-', expand=True)
    # df1.to_csv(real_apple_price)
    pd.options.mode.chained_assignment = None  # default='warn'
    for i in range(len(df1['Month'])):
        if df1['Month'][i][0] == '0':
            a = df1['Month'][i][1:]
            df1['Month'][i] = a
        if df1['Day'][i][0] == '0':
            df1['Day'][i] = df1['Day'][i][1:]
    df1.apply(pd.to_numeric, errors='ignore')
    df1['timestamp'] = pd.to_datetime(arg=df1[['Day', 'Month', 'Year']], format='%d/%m/%Y')

    joined = pd.merge(df, df1, how='left', left_on=['Year', 'Month', 'Day'], right_on=['Year', 'Month', 'Day'])

    joined_path = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/New_lists/%s.csv'
    comp_joined_path = joined_path % company_name

    joined['yield'] = joined['price_target'] / joined['open'] - 1
    joined = joined[['Year', 'Month', 'Day', 'stock', 'brokerage', 'yield', 'price_target', 'open', 'timestamp_x']]
    # joined.dropna(subset=['open'], inplace=True)

    return joined.to_csv(comp_joined_path)


for company in companies:
    print(company)
    clean(company)


