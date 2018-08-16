import csv
from datetime import timedelta, datetime

import pandas as pd
import pickle


def fetch_delta_data(delta_in_days, quarter_datetime, min_stock, min_rec):
    delta_datetime = quarter_datetime - timedelta(days=delta_in_days)
    df = pd.read_csv('/Users/amirgavrieli/PycharmProjects/Weizmann - scraper/uspr-master/ratings/Daw_jones_30/'
                     'New_lists/All_companies.csv')
    df_subset = df[(pd.to_datetime(df["timestamp_x"]) >= delta_datetime)
                   & (pd.to_datetime(df["timestamp_x"]) <= quarter_datetime)]
    df_subset = df_subset.groupby((["brokerage", "stock"]))["timestamp_x"].max().reset_index()
    df_subset = df_subset.merge(df[["brokerage", "stock", "timestamp_x", "yield"]],
                                on=["brokerage", "stock", "timestamp_x"])
    df_subset.drop_duplicates(inplace=True)
    df_subset = df_subset[["brokerage", "stock", "yield"]]
    final_matrix = df_subset.pivot(index='brokerage', columns='stock')
    final_mat2 = final_matrix['yield']
    final_mat2 = final_mat2[final_mat2.apply(lambda x: x.isnull().sum(), axis='columns') > min_stock]
    # final_mat2 = final_mat2.drop(final_mat2.columns[final_mat2.apply(lambda col: col.notnull().sum() < min_rec)], axis=1)

    path = "/Users/amirgavrieli/Desktop/final_matrix" +' ' + str(quarter_datetime) +' delta is=' + str(delta_in_days) \
           + '.csv'
    final_mat2.to_csv(path)
    with open("/Users/amirgavrieli/Desktop/final_matrix.pkl", "wb") as f:
        pickle.dump(final_mat2, f)


def read_and_print_matrix(file_path):
    with open(file_path, "rb") as f:
        matrix = pickle.load(f)
        print(matrix)



if __name__ == '__main__':
    fetch_delta_data(180, datetime(2017, 3, 3), min_stock = 20, min_rec= 7)
    read_and_print_matrix("/Users/amirgavrieli/Desktop/final_matrix.pkl")
