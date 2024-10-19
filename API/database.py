from __future__ import annotations

import logging
from datetime import datetime

from pymongo import MongoClient, errors

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="ImageDB"):
        """
        Initialize a Database object.

        Args:
            uri (str): The uri of the MongoDB server. Defaults to 'mongodb://localhost:27017/'.
            db_name (str): The name of the MongoDB database. Defaults to 'ImageDB'.
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            logger.info("Successfully connected to MongoDB.")
        except errors.ConnectionError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def find(self, collection, query=None):
        """
        Find documents in the given collection.

        Args:
            collection (str): The name of the collection to search.
            query (dict): The query to filter the documents by. Defaults to None.

        Returns:
            pymongo.cursor.Cursor: A cursor pointing to the results of the query.
        """
        try:
            return self.db[collection].find(query)
        except errors.PyMongoError as e:
            logger.error(f"Error finding documents in {collection}: {e}")
            return None

    def insert_one(self, collection, document):
        """
        Insert a single document into the given collection.

        Args:
            collection (str): The name of the collection to insert into.
            document (dict): The document to insert.

        Returns:
            pymongo.results.InsertOneResult: The result of the insertion.
        """
        try:
            return self.db[collection].insert_one(document)
        except errors.PyMongoError as e:
            logger.error(f"Error inserting document into {collection}: {e}")
            return None

    def find_one(self, collection, filter, projection=None):
        """
        Find a single document in the given collection.

        Args:
            collection (str): The name of the collection to search.
            filter (dict): The query to filter the documents by.
            projection (dict, optional): The fields to include in the result. Defaults to None.

        Returns:
            dict: The document that matches the query, or None if no documents match.
        """
        try:
            return self.db[collection].find_one(filter=filter, projection=projection)
        except errors.PyMongoError as e:
            logger.error(f"Error finding document in {collection}: {e}")
            return None

    def find_one_and_delete(self, collection, query):
        """
        Find a single document and delete it in the given collection.

        Args:
            collection (str): The name of the collection to search.
            query (dict): The query to filter the documents by.

        Returns:
            dict: The document that matches the query, or None if no documents match.
        """
        try:
            return self.db[collection].find_one_and_delete(query)
        except errors.PyMongoError as e:
            logger.error(f"Error deleting document in {collection}: {e}")
            return None

    def update_one(self, collection, query, update):
        """
        Update a single document in the given collection.

        Args:
            collection (str): The name of the collection to update.
            query (dict): The query to filter the documents by.
            update (dict): The update to apply to the matching document.

        Returns:
            pymongo.results.UpdateResult: The result of the update.
        """
        try:
            return self.db[collection].update_one(query, update)
        except errors.PyMongoError as e:
            logger.error(f"Error updating document in {collection}: {e}")
            return None

    def vector_search(self, collection, embedding):
        """
        Perform a vector similarity search on the given collection.

        Args:
            collection (str): The name of the collection to search.
            embedding (list): The vector to search for.

        Returns:
            list: A list of documents with the closest embedding to the query vector, sorted by score.
        """
        try:
            result = self.db[collection].aggregate(
                [
                    {
                        "$vectorSearch": {
                            "index": "vector_index",
                            "path": "embedding",
                            "queryVector": embedding,
                            "numCandidates": 20,
                            "limit": 20,
                        },
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "Name": 1,
                            "Image": 1,
                            "score": {"$meta": "vectorSearchScore"},
                        },
                    },
                ],
            )
            result_arr = [i for i in result]
            return result_arr
        except errors.PyMongoError as e:
            logger.error(
                f"Error performing vector search in {collection}: {e}")
            return []
