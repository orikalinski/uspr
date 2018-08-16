import pandas as pd
import numpy as np
import csv
import datetime


# for each event_date and delta we find the price for each stock for that closest event_date
def delta_price(event_date, delta, stock):  # event_date = 'YYYY-MM-DD' , delta = int, stock = 'Name_of_stock'

    price_path = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/' \
                 'Real_prices_Alpha_vantage/daily_%s.csv'
    stock_price_path = price_path % stock
    df = pd.read_csv(stock_price_path)
    l2 = []
    for i in range(len(df['timestamp'])):
        tmp = datetime.datetime.strptime(df['timestamp'][i], '%Y-%m-%d')
        l2.append(tmp)
    df['date'] = l2
    event_date1 = datetime.datetime.strptime(event_date, '%Y-%m-%d')
    diff = (df['date'] - event_date1)
    closest_event_date = df['date'][abs((df['date'] - event_date1)) == min(abs(diff))]
    closest_price = df['open'][closest_event_date.index[0]]

    stock_recommends = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/' \
                       'After_price_change/%s.csv'
    stock_path = stock_recommends % stock
    l1 = []
    df1 = pd.read_csv(stock_path)
    df1.dropna(subset=['date'], inplace=True)
    for i in range(len(df1['date'])):
        tmp1 = datetime.datetime.strptime(df1['date'][i], '%m/%d/%Y')
        l1.append(tmp1)
    df1['date'] = l1

    diff_days = (event_date1 - df1['date']).days
    # a = pd.Timedelta('1 days')
    # diff = diff / a
    df1['Delta'] = diff_days

    df2 = df1[df1.Delta < delta]
    df2 = df2[df2.Delta > 0]
    df2['stock'] = stock
    df2.dropna(subset=['price_target'], inplace=True)
    df2['Yield'] = df2['price_target'] / closest_price
    return df2


def test():
    event_date = '2017-08-01'
    # stock = 'INTC'
    delta = 90
    # def initial_matrix(event_date, delta):

    company_list = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/daw_jones_30_links.csv'

    with open(company_list) as f:
        reader = csv.reader(f)
        companies = [row[0] for row in reader]

    full_list = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/' \
                'New_lists/{0}_delta_{1}.csv'
    str_delta = str(delta)
    path = full_list.format(event_date, str_delta)

    headers = ['', 'event_date', 'brokerage', 'stock', 'action', 'rating', 'price_target', 'event_datetime', 'Delta']
    # with open(path, 'a') as all:
    #     writer = csv.writer(all)
    #     writer.writerow(headers)
    #
    # dt = pd.read_csv(path)

    dt = pd.DataFrame(columns=headers)

    for company in companies:
        df = delta_price(event_date, delta, company)
        dt = dt.append(df)

    dt2 = dt.drop_duplicates(subset=['brokerage', 'stock'], keep='first')
    unique_brokerage = [brokerage for brokerage in dt2.brokerage.unique()]

    mat = pd.DataFrame(columns=companies)

    # initial_matrix(event_date, delta)
    # s.to_csv('/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/
    # New_lists/90_delta_2017-08-01.csv')


if __name__ == '__main__':
    test()
