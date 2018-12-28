#!encoding:utf-8

import pandas as pd


def name_code():
    data = pd.read_csv('/root/ecoinfor/recommendation/name_code.csv', dtype = str)
    res = dict()
    for i in data.iterrows():
        res[str(i[1]['stockcode'])] = i[1]['stockname']
    return res
