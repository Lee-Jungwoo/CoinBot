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
        collection.insert_items(docs)

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
        self.mongodb.get_current_collection().delete_many({})
        self.mongodb.insert_item(self.mongodb.get_current_db_name(),
                                 self.mongodb.get_current_collection_name(),
                                 {"currency": "BTC", "price": 10000})
        assert self.mongodb.get_current_collection().find_one()

    def test_insert_many(self):
        print(inspect.stack()[0][3])
        self.mongodb.get_current_collection().delete_many({})
        self.mongodb.insert_items(self.mongodb.get_current_db_name(),
                                  self.mongodb.get_current_collection_name(),
                                  [{"currency": "BTC", "price": 10000},
                                            {"currency": "ETH", "price": 2000},
                                             {"currency": "LTC", "price": 240}])

        self.assertEqual(3, self.mongodb.get_current_collection().count_documents({}))

    def test_

if __name__ == '__main__':
    unittest.main()
