import os

import pymongo
from urllib.parse import quote_plus


class Database(object):
    user = "complex"
    password = "passw0rd"
    socket_path = "127.0.0.1:27017"
    URI = "mongodb://%s:%s@%s" % (quote_plus(user), quote_plus(password), socket_path)
    AWARE = True
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI, tz_aware=Database.AWARE)
        Database.DATABASE = client['complex']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection, query, data):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)
