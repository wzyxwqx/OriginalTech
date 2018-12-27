"""
this code is to add another column in the database crawled_news.sina_news, 
which shows the related stock about the news.
"""
import pymysql
import pandas as pd
stocknamefile="stocklist.csv"
data=pd.read_csv(stocknamefile,dtype={'code':str})
stocklist=data['stockname']
stockcode=data['code']
tablelist=["news"]
class news_connector:
    data=pd.read_csv(stocknamefile)
    def __init__(self,tablename):
        self.db=pymysql.connect(host = "localhost", user = "mlf", passwd = "mashiro120", db = "crawled_news", charset = "utf8")
        self.tablename=tablename
        self.cursor=self.db.cursor()

    def related_stcok(self,content):
        temp=" "
        if content!=None:
            for i in range(len(stocklist)):
                if stocklist[i] in content:
                    temp+=" "+stockcode[i]
        return temp
    def update(self):
        sql="select MAX(id) from "+self.tablename
        self.cursor.execute(sql)
        maxidtemp=self.cursor.fetchone()
        maxid=maxidtemp[0]
        turn=maxid//3000+1
        for i in range(1,turn+1):
            tempmin=(i-1)*3000
            tempmax=i*3000
            sql="select id,content from "+self.tablename+" where id>="+str(tempmin)+" and id<"+str(tempmax)+" and keystock is NULL"
            self.cursor.execute(sql)
            results=self.cursor.fetchall()
            try:
                for row in results:
                    sql="UPDATE "+self.tablename+" SET keystock=\""+self.related_stcok(row[1])+"\" WHERE id="+str(row[0])
                    print(sql)
                    self.cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
        
        self.cursor.close()
        self.db.close()


        

def main():
    for i in range(len(tablelist)):
        news_connector(tablelist[i]).update()

if __name__=="__main__":
    main()
