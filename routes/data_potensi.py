from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from models.models import Dapot
from config.dbfull import dapot_connection
from schemas.schemas import DataPotensi, DatasPotensi
from bson import ObjectId
import pymongo

dapot = APIRouter(tags=["Data Potensi"])

@dapot.get('/')
async def find_dapot():
    dapot_cursor = dapot_connection.local.dapot.find()
    print(dapot_cursor)
    dapot_list = list(dapot_cursor)
    if len(dapot_list) > 0:
        print(DataPotensi(dapot_list[0]))
    else:
        print("List 'dapot_list' kosong. Tidak ada elemen yang dapat ditampilkan.") 
    return DatasPotensi(dapot_list)

@dapot.post('/')
async def create_dapot(dapot : Dapot):
    dapot_connection.local.dapot.insert_one(dict(dapot))
    return DatasPotensi(dapot_connection.local.dapot.find())

@dapot.put('/{id}')
async def dapot_student(id, dapot: Dapot):
    updated_dapot = dapot_connection.local.dapot.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(dapot)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return DataPotensi(updated_dapot)

@dapot.delete('/{id}')
async def delete_dapot(id):
    dapot = dapot_connection.local.dapot.find_one_and_delete({"_id": ObjectId(id)})
    if dapot:
        return DataPotensi(dapot)
    else:
        return {"message": "Data Potensi not found"}    
