from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI ="mongodb://localhost:27017"

async def get_database():
    client = AsyncIOMotorClient(MONGO_URI)
    database = client.get_database('dira_abinawa-all')
    return database