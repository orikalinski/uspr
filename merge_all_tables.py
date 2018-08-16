import pandas as pd
import numpy as np
import csv

joined_path = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/New_lists/%s.csv'
company = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30_links/New_lists/%s.csv'
company_list = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/daw_jones_30_links.csv'


with open(company_list) as f:
    reader = csv.reader(f)
    companies = [row[0] for row in reader]

comp0 = company % companies[0]
df0 = pd.read_csv(comp0)

comp1 = company % companies[1]
df1 = pd.read_csv(comp1)

dfs = [df0, df1]
result = pd.concat(dfs)

merged12 = company_list % 'merged12'
result.to_csv(merged12)


company = '/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30_links/New_lists/MMM.csv'
