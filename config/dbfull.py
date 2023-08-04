from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = MongoClient("<mongoDB-URL>")
db = client.get_database('dira_abinawa-all')
MONGO_URI ="<mongoDB-URL>"

async def get_database():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client.get_database('dira_abinawa-all')
    return database