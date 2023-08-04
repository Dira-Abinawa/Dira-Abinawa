from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = MongoClient("mongodb+srv://RDGalihRakasiwi:fkSeIRIz0aQ3NfVf@cluster0.ni5ltny.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('dira_abinawa-all')
MONGO_URI ="mongodb+srv://RDGalihRakasiwi:fkSeIRIz0aQ3NfVf@cluster0.ni5ltny.mongodb.net/?retryWrites=true&w=majority"

async def get_database():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client.get_database('dira_abinawa-all')
    return database