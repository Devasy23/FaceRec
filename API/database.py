from datetime import datetime

from pymongo import MongoClient


class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="ImageDB"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def find(self, collection, query=None):
        return self.db[collection].find(query)

    def insert_one(self, collection, document):
        return self.db[collection].insert_one(document)

    def find_one(self, collection, filter, projection=None):
        return self.db[collection].find_one(filter=filter, projection=projection)

    def find_one_and_delete(self, collection, query):
        return self.db[collection].find_one_and_delete(query)

    def update_one(self, collection, query, update):
        return self.db[collection].update_one(query, update)
    def find_similar_vectors(self, collection, embedding, n):
        """
        Find the top n most similar vectors in the database to the given embedding.
        :param collection: The MongoDB collection to search in.
        :param embedding: The input vector.
        :param n: The number of top similar vectors to return.
        :return: The top n most similar vectors from the database.
        """
        pipeline = [
            {
                "$addFields": {
                    "distance": {
                        "$sqrt": {
                            "$reduce": {
                                "input": {"$zip": {"inputs": ["$embedding", embedding]}},
                                "initialValue": 0,
                                "in": {"$add": ["$$value", {"$pow": [{"$subtract": ["$$this.0", "$$this.1"]}, 2]}]}
                            }
                        }
                    }
                }
            },
            {"$sort": {"distance": 1}},
            {"$limit": n}
        ]
        return list(self.db[collection].aggregate(pipeline))
