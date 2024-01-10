import inspect
import unittest
import autotrading.db.mongodb_handler as mongodb_handler


class MongoDBHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.mongodb = mongodb_handler.MongoDBHandler("local", "coiner_test", "price_info")
        collection = self.mongodb.get_current_collection()

        collection.delete_many({})
        docs = [
            {"currency": "btc", "price": 10000},
            {"currency": "eth", "price": 1000},
            {"currency": "ltc", "price": 240}
        ]
        collection.insert_many(docs)

    def tearDown(self):
        pass

    def test_set_db_collection(self):
        pass
        print(inspect.stack()[0][3])
        self.mongodb.set_db_collection("trader_test", "trade_status")
        self.assertEqual(self.mongodb.get_current_db_name(), "trader_test")
        self.assertEqual(self.mongodb.get_current_collection_name(), "trade_status")

    def test_get_current_db_name(self):
        print(inspect.stack()[0][3])
        self.assertEqual(self.mongodb.get_current_db_name(), "coiner_test")

    def test_get_current_collection_name(self):
        print(inspect.stack()[0][3])
        self.assertEqual(self.mongodb.get_current_collection_name(), "price_info")

    def test_insert_one(self):
        print(inspect.stack()[0][3])
        self.mongodb.insert_item("coiner_test",
                                 "price_info",
                                 {"currency": "BTC", "price": 10000})
        self.assertEqual(4, self.mongodb.get_current_collection().count_documents({})) # (3 + document added in this test) => 4

    def test_insert_many(self):
        print(inspect.stack()[0][3])
        self.mongodb.insert_items("coiner_test",
                                  "price_info",
                                  [{"currency": "BTC_", "price": 10099900},
                                            {"currency": "ETH_", "price": 2009990},
                                             {"currency": "LTC_", "price": 249990}])

        self.assertEqual(6, self.mongodb.get_current_collection().count_documents({})) # (3 + documents added in this test) => 6

    def test_delete_one(self):
        print(inspect.stack()[0][3])
        result = self.mongodb.delete_item("coiner_test", "price_info", {"price": {"$gt": 10}})
        if result < 0 or result > 1:
            raise AssertionError("")

    def test_delete_many(self):
        print(inspect.stack()[0][3])
        result = self.mongodb.delete_items("coiner_test", "price_info", {"price": {"$gt": 10}})
        if result < 0 or result > 3:
            raise AssertionError("")


if __name__ == '__main__':
    unittest.main()
