# Configuration settings for database connections
DB_CONFIG = {
# URI for connecting to the local MongoDB instance
    "local_uri": "mongodb://localhost:27017/",
    "atlas_uri": "<Your MongoDB Atlas Connection String Here>",
    "db_name": "ImageDB",
    "USE_ATLAS": False
}
# URI for connecting to MongoDB Atlas - replace <Your MongoDB Atlas Connection String Here> with your actual connection string.
# You can obtain this string from your MongoDB Atlas dashboard under the 'Connect' section of your cluster.
# Name of the database to be used
# Flag to toggle the use of MongoDB Atlas; set to True to use Atlas or False to use the local database
