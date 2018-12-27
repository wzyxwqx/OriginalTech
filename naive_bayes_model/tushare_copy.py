import pandas as pd
import datetime

def get_stock_data(stockcode, date):
    csv_path = "/root/originaltech/stock_data/localts/data/" + date + ".csv"
    table = pd.read_csv(csv_path, converters={'stockname':str})
    for row in table.iterrows():
        if stockcode == row[1][13]:
            return row[1]
    print(stockcode + " not found in " + date)
    return pd.DataFrame()

def get_stocklist_data(stocklist, date, num_err):
    if num_err >= 5:
        return(0)
    csv_path = "/root/originaltech/stock_data/localts/data/" + date + ".csv"
    table = pd.read_csv(csv_path, converters={'stockname':str})
    num_stock = len(stocklist)
    num_shot = 0
    total_pchange = 0
    for row in table.iterrows():
        if row[1][13] in stocklist:
            num_shot += 1
            if row[1].p_change > 0.5:
                total_pchange += 1
            else:
                total_pchange -= 1
    if(num_shot == 0):
        new_date = datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=1)
        return(get_stocklist_data(stocklist, new_date.strftime("%Y-%m-%d"), num_err+1))
    if total_pchange > 0:
        return(1)
    else:
        return(0)

