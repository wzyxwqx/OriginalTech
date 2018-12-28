import pymysql


class MysqlConnector:
    def __init__(self):
        self._database = pymysql.connect(host = '165.227.30.65', user = 'mlf', passwd = 'mashiro120', db = 'crawled_news', charset = 'utf8')
        self._cursor = self._database.cursor()


    def fetchdata(self, checksql):
        try:
            self._cursor.execute(checksql)
        except Exception as e:
            raise e
        result = self._cursor.fetchall()
        if len(result) == 0:
            raise ValueError('Invalid request.')
        return result

    def insertdata(self, insertsql):
        try:
            self._cursor.execute(insertsql)
        except Exception as e:
            raise e
        self._database.commit()
        return True
