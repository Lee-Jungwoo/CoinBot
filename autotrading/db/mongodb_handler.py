from pymongo import MongoClient
from pymongo import cursor
import configparser
from pprint import pprint as p
import autotrading.db.DBHandler as DBHandler

CONFIGPATH = '/Users/ijeong-u/PycharmProjects/CoinBot/conf/config.ini'


class MongoDBHandler(DBHandler.DBHandler):
    _client = None
    _db = None
    _collection = None

    def __init__(self, mode="local", db_name=None, collection_name=None):
        """

        :param mode: string, either "local" or "remote"
        :param db_name: string.
        :param collection_name: string.
        """
        p = configparser.ConfigParser()
        p.read(CONFIGPATH)

        local_ip = p['MONGODB']['local_ip']
        port = p['MONGODB']['port']

        if mode == "remote":
            raise NotImplementedError("MongoDBHandler for remote db not implemented yet")
        else:
            self._client = MongoClient("mongodb://" + local_ip + ":" + port + "/")

        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def set_db_collection(self, db_name=None, collection_name=None):
        """
        similar to 'use' in mongosh.
        change current database and collection.

        :param db_name: required, string
        :param collection_name: not required, string
        :return: None
        """
        if db_name is None:
            raise Exception("db_name is required")

        self._db = self._client[db_name]

        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db(self):
        """

        :return: current DB object. not the name!!!!
        """
        return self._db

    def get_current_db_name(self):
        """

        :return: current db's name in str.
        """
        return self._db.name

    def get_current_collection(self):
        """

        :return: current collection object. not the name!
        """
        return self._collection

    def get_current_collection_name(self):
        """

        :return: current collection's name in str.
        """
        return self._collection.name

    def get_client(self):
        """

        :return: MongoDB client object. Similar to JDBC Connection.
        """
        return self._client

    def insert_item(self, db_name, collection_name, item):
        """
        :param db_name: string, the name of the database
        :param collection_name: string, name of the collection.
        :param item: dictionary to be registered to the collection
        :return: None
        """
        db = self._client[db_name]
        collection = db[collection_name]
        if collection.insert_one(item).acknowledged:
            print("inserted 1 record to db.")

    def insert_items(self, db_name, collection_name, items):
        """

        :param db_name: string, the name of the database
        :param collection_name: string, name of the collection.
        :param items: list of dictionaries to be registered to the collection
        :return: None
        """

        db = self._client[db_name]
        collection = db[collection_name]
        if collection.insert_many(items).acknowledged:
            print("inserted {} record(s) to db.".format(len(items)))

    def delete_item(self, db_name, collection_name, filter_dic):
        """
        여러 개를 찾으면 처음 find 하나만 지움
        :param db_name:
        :param collection_name: collection name in str.
        :param filter_dic: filter dictionary.
        :return: number of deleted record (0 or 1)
        """

        db = self._client[db_name]
        collection = db[collection_name]

        if filter_dic is None or filter_dic == {}:
            raise TypeError("filter_dic must not be none.")

        result = collection.delete_one(filter_dic)
        if result.acknowledged:
            print("deleted {} record.".format(result.deleted_count))

        return result.deleted_count

    def delete_items(self, db_name, collection_name, filter_dic):
        """
        맞는거 다 지움
        :param db_name:
        :param collection_name: collection name in str.
        :param filter_dic: filter dictionary.
        :return: number of deleted records
        """

        db = self._client[db_name]
        collection = db[collection_name]

        if filter_dic is None or filter_dic == {}:
            raise TypeError("filter_dic must not be none.")

        result = collection.delete_many(filter_dic)

        if result.acknowledged:
            print("deleted {} records.".format(result.deleted_count))

        return result.deleted_count

    def find_item(self, db_name, collection_name, filter_dic):
        """
        맞는것중 하나만 찾음
        :param db_name: string
        :param collection_name: string
        :param filter_dic: filter dictionary
        :return: dictionary of the result record(document in this case)
        """

        db = self._client[db_name]
        collection = db[collection_name]

        #
        # if filter_dic is None or filter_dic == {}:
        #     raise TypeError("filter_dic must not be none.")

        result = collection.find_one(filter_dic, projection={"_id": False})
        return result

    def find_items(self, db_name, collection_name, filter_dic):
        """
        다 찾아서 리턴
        :param db_name:
        :param collection_name:
        :param filter_dic:
        :return:
        """
        db = self._client[db_name]
        collection = db[collection_name]

        result = collection.find(filter=filter_dic, projection={"_id": False}, cursor_type = cursor.CursorType.EXHAUST)

        return result
