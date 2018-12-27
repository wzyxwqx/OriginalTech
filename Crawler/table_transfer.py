#!encoding:utf-8
import pymysql

db = pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
cursor = db.cursor()

if __name__ == "__main__":
    check_sql = "select * from nbd_news"
    cursor.execute(check_sql)
    table = cursor.fetchall()
    count = 0
    for row in table:
        title = row[1]
        url = row[2]
        if row[3] == None:
            content = ''
        else:
            content = row[3]
        if row[4] == None:
            time = ''
        else:
            time = row[4]
        if row[5] == None:
            abstract = ''
        else:
            abstract = row[5]
        if row[6] == None:
            source = ''
        else:
            source = row[6]
        '''
        if row[7] == None:
            topic = ''
        else:
            topic = row[7]
        if row[6] == None:
            keystock = ''
        else:
            keystock = row[6]
        '''
        insert_sql = "insert into news (title, url, content, time, source, abstract, website) values ('" + title + "', '" + url + "', '" + content + "', '" + str(time) + "', '" + source + "', '" + abstract + "', '每经网')"
        cursor.execute(insert_sql)
        db.commit()
        count += 1
        if count % 1000 == 0:
            print(count)
    print("finish")

