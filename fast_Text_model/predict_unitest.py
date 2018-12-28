from predict_test import predict
import unittest

class TestPredict(unittest.TestCase):
    def setUp(self):
        self.Predict = predict()
    def tearDown(self):
        self.Predict=None
    def testConn(self):
        self.Predict.conn()
        self.assertTrue(self.Predict.cursor!=None)
        self.assertTrue(len(self.Predict.news_list)!=0)
        
    def testGetLr(self):
        self.Predict.get_logistic()
        self.assertTrue(self.Predict.cls!=None)
    def testGetfinco(self):
        self.Predict.get_fin_co()
        self.assertTrue(self.Predict.fin_co!=None)
    def testPredictData(self):
        self.Predict.predict_data()
        self.assertTrue(self.Predict.recomand==dict())
    def testStoreRecommand(self):
        self.Predict.store_recomand()

if __name__=="__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestPredict("testConn"))
    suite.addTest(TestPredict("testGetLr"))
    suite.addTest(TestPredict("testGetfinco"))
    suite.addTest(TestPredict("testPredictData"))
    suite.addTest(TestPredict("testStoreRecommand"))
    runner = unittest.TextTestRunner()
    runner.run(suite)


