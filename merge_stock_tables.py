import pandas as pd
import numpy as np
import csv


company_list = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/daw_jones_30_links.csv'
company_path = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/New_lists/%s.csv'
All_companies = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/New_lists/All_companies.csv'

with open(company_list) as f:
    reader = csv.reader(f)
    companies = [row[0] for row in reader]

companies_path = [company_path % path for path in companies]

headers = ['', 'Year','Month','Day','stock','brokerage','yield','price_target', 'open']
with open(All_companies, 'a') as all:
    writer = csv.writer(all)
    writer.writerow(headers)

All = pd.read_csv(All_companies)
for company in companies_path:
    tmp = pd.read_csv(company)
    tmp = tmp.drop(['Unnamed: 0'], axis=1)
    All = pd.concat([All, tmp])
    if 'Unnamed: 0' in All:
        All = All.drop(['Unnamed: 0'], axis=1)

All.dropna(subset=['yield'], inplace=True)

All.to_csv(All_companies)



# verticalStack = pd.concat(, , axis=0)


