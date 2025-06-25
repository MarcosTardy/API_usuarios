from pymongo import MongoClient

db_client = MongoClient(
    "mongodb+srv://test_users:test_users@cluster0.ljpphku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = db_client.test_users
users_collection = db.users
