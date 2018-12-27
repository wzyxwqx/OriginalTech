import pandas as pd
from datetime import datetime
import math

def get_stock_data(stockcode, date):
    csv_path = "/root/originaltech/stock_data/localts/data/" + date + ".csv"
    table = pd.read_csv(csv_path, converters={'stockname':str})
    for row in table.iterrows():
        if stockcode == row[1][13] and not math.isnan(row[1][0]):
            return row[1]
    print(stockcode + " not found in " + date)
    return None
