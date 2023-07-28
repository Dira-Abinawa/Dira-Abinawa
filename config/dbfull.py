from pymongo import MongoClient

client = MongoClient("mongodb+srv://RDGalihRakasiwi:fkSeIRIz0aQ3NfVf@cluster0.ni5ltny.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('dira_abinawa-all')
dkr_connection = db.get_collection('dewan_kerja_ranting')
news_connection = db.get_collection('news')
coment_connection = db.get_collection('coment')
sch_connection = db.get_collection('schools')
dapot_connection = db.get_collection('data_potensi')
activity_connection = db.get_collection('activity')
opinion_connection = db.get_collection('opinion')

users_connection = db.get_collection('users')

# {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }
