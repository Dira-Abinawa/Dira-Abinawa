from pymongo import MongoClient

client = MongoClient("mongodb+srv://RDGalihRakasiwi:fkSeIRIz0aQ3NfVf@cluster0.ni5ltny.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('dira_abinawa-all')
dkr_connection = db.get_collection('dewan_kerja_ranting')
news_connection = db.get_collection('news')
sch_connection = db.get_collection('schools')
dapot_connection = db.get_collection('data_potensi')
activity_connection = db.get_collection('activity')
opinion_connection = db.get_collection('opinion')