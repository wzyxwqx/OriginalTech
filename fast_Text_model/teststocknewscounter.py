import unittest
from stocknewscounter import StockNewsCounter


class TestStockNewsCounter(unittest.TestCase):
    def setUp(self):
        self.stockNewsCounter = StockNewsCounter()
        self.assertTrue(self.stockNewsCounter.conn)
        self.assertTrue(len(self.stockNewsCounter.news) == 0)
        self.assertTrue(len(self.stockNewsCounter.stock_total) == 0)
        self.assertTrue(len(self.stockNewsCounter.stock_good) == 0)
        self.assertTrue(len(self.stockNewsCounter.stock_bad) == 0)

    def testfetcherror(self):
        with self.assertRaises(Exception):
            self.stockNewsCounter.fetch(-1)

    def testcount(self):
        self.stockNewsCounter.count()
        self.assertTrue(len(self.stockNewsCounter.stock_total) == 0)
        self.assertTrue(len(self.stockNewsCounter.stock_good) == 0)
        self.assertTrue(len(self.stockNewsCounter.stock_bad) == 0)

    def testinsert(self):
        with self.assertRaises(Exception):
            self.stockNewsCounter.insert()

if __name__ == "__main__":
    # create test suite
    suite = unittest.TestSuite()
    suite.addTest(TestStockNewsCounter("testfetcherror"))
    suite.addTest(TestStockNewsCounter("testcount"))
    suite.addTest(TestStockNewsCounter("testinsert"))
    # execute test
    runner = unittest.TextTestRunner()
    runner.run(suite)
