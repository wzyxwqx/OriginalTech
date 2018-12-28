import pymysql
import string
import urllib
import requests
import time
from datetime import datetime

#db = pymysql.connect(user = "mlf", passwd = "mashiro120", db = "stock_data", charset = "utf8")
#cursor = db.cursor()

def is_sh(stockcode):
    if stockcode[0] == '6':
        return True
    else:
        return False

def is_sz(stockcode):
    if stockcode[0] in ('0', '2', '3'):
        return True
    else:
        return False

def sina_latest_data(stockcode_list):
    url = "http://hq.sinajs.cn/list="
    for stockcode in stockcode_list:
        if is_sh(stockcode):
            code = 'sh' + stockcode
        elif is_sz(stockcode):
            code = 'sz' + stockcode
        else:
            return 'Unlisted code ' + stockcode + ' in sh or sz'
        url += code + ','
    url = url.strip(',')
    url_response = urllib.request.urlopen(url).read().decode('utf-8', 'ignore').split('\n')
    response = dict()
    for line in url_response:
        if len(line) == 0:
            continue
        stockcode = line.split('=')[0].split('s')[2][1:]
        data = line.strip('";').split('"')[1].split(',')
        res = dict()
        res['chi_name'] = data[0]
        res['open'] = data[1]
        res['yes_close'] = data[2]
        res['cur_price'] = data[3]
        res['high'] = data[4]
        res['low'] = data[5]
        res['vol'] = data[8]
        # up
        res['turn_vol'] = data[9]
        res['buy1_vol'] = data[10]
        res['buy1'] = data[11]
        res['buy2_vol'] = data[12]
        res['buy2'] = data[13]
        res['buy3_vol'] = data[14]
        res['buy3'] = data[15]
        res['buy4_vol'] = data[16]
        res['buy4'] = data[17]
        res['buy5_vol'] = data[18]
        res['buy5'] = data[19]
        res['sell1_vol'] = data[20]
        res['sell1'] = data[21]
        res['sell2_vol'] = data[22]
        res['sell2'] = data[23]
        res['sell3_vol'] = data[24]
        res['sell3'] = data[25]
        res['sell4_vol'] = data[26]
        res['sell4'] = data[27]
        res['sell5_vol'] = data[28]
        res['sell5'] = data[29]
        res['date'] = data[30]
        res['time'] = data[31]
        response[stockcode] = res
    return response

def netease_historical_data(stockcode):
    now = datetime.now()
    nowtime = now.strftime('%Y%m%d')
    url = 'http://quotes.money.163.com/service/chddata.html?code='
    if is_sh(stockcode):
        code = '0' + stockcode
    elif is_sz(stockcode):
        code = '1' + stockcode
    else:
        return 'Unlisted code ' + str(stockcode) + ' in sh or sz'
    url += code
    url += '&start=20000101&end=' + nowtime + '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;'
    historical_data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore').split('\r\n')[1:]
    response = dict()
    for line in historical_data:
        time = line.split(',')[0]
        if time == '':
            continue
        res = dict()
        res['close'] = line.split(',')[3]
        res['high'] = line.split(',')[4]
        res['low'] = line.split(',')[5]
        res['open'] = line.split(',')[6]
        res['pre_close'] = line.split(',')[7]
        res['change'] = line.split(',')[8]
        res['change_percentage'] = line.split(',')[9]
        res['vol'] = line.split(',')[10]
        response[time] = res
    return response

def xueqiu_historical_data(stockcode):
    now = datetime.now()
    nowtime = now.strftime('%Y-%m-%d %H:%M:%S')
    timestamp = str(time.mktime(now.timetuple()))
    end_time = timestamp.split('.')[0] + '000'
    headers = {
            "Accept" : "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9",
            "cache-control" : "no-cache",
            "Connection" : "keep-alive",
            "Cookie" : "aliyungf_tc=AQAAALpBylKYjA4AsLc5cWOtI0XvXlDf; xq_a_token=229a3a53d49b5d0078125899e528279b0e54b5fe; xq_a_token.sig=oI-FfEMvVYbAuj7Ho7Z9mPjGjjI; xq_r_token=8a43eb9046efe1c0a8437476082dc9aac6db2626; xq_r_token.sig=Efl_JMfn071_BmxcpNvmjMmUP40; __utma=1.461614876.1522589407.1522589407.1522589407.1; __utmc=1; __utmz=1.1522589407.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_1db88642e346389874251b5a1eded6e3=1522589408; u=311522589410819; device_id=a570575343f72340971cbc6acbb00ba7; s=f314ecnpa7; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1522589950",
            "Host" : "xueqiu.com",
            "Referer" : "https://xueqiu.com/hq",
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
            "X-Requested-With" : "XMLHttpRequest"}
    if is_sh(stockcode):
        code = 'SH' + stockcode
    elif is_sz(stockcode):
        code = 'SZ' + stockcode
    else:
        return 'Unlisted code ' + str(stockcode) + ' in sh or sz'
    url = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol=' + code + '&period=1day&type=before&begin=978278400000&end=' + end_time + '&_=' + end_time
    data = requests.get(url, headers = headers)
    print(data)
