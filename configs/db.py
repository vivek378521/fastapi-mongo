from pymongo import MongoClient
client = MongoClient()
db = client.kimo
collection = db["courses"]