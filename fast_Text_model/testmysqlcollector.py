import unittest
from mysqlconnector import MysqlConnector


class TestMysqlConnector(unittest.TestCase):
    def setUp(self):
        self.mysqlConnector = MysqlConnector()
        self.assertTrue(self.mysqlConnector._database)
        self.assertTrue(self.mysqlConnector._cursor)

    def testCollect(self):
        check_sql = "select title, content, keystock, time from news where keystock != '' order by time desc limit 1"
        res = self.mysqlConnector.fetchdata(check_sql)
        self.assertTrue(len(res) > 0)

    def testCollectError(self):
        check_sql = ""
        with self.assertRaises(Exception):
            res = self.mysqlConnector.fetchdata(check_sql)

    def testInsert(self):
        insert_sql = ""
        with self.assertRaises(Exception):
            self.mysqlConnector.insertdata(insert_sql)

if __name__ == "__main__":
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestMysqlConnector("testCollect"))
    suite.addTest(TestMysqlConnector("testCollectError"))
    suite.addTest(TestMysqlConnector("testInsert"))
    # execute test
    runner = unittest.TextTestRunner()
    runner.run(suite)
