from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from models.models import Dapot
from config.dbfull import get_database
from routes.login import get_current_active_user, non_admin_required
from schemas.schemas import DataPotensi, DatasPotensi
from bson import ObjectId
import pymongo

dapot = APIRouter(tags=["Data Potensi"])

@dapot.get('/')
async def find_dapot(database = Depends(get_database)):
    db_dapot = database["dapot"]
    dapot_cursor = db_dapot.find()
    dapot_list = await dapot_cursor.to_list(length=None)
    return DatasPotensi(dapot_list)

@dapot.post('/')
async def create_dapot(dapot: Dapot, database=Depends(get_database)):
    db_dapot = database["dapot"]
    await db_dapot.insert_one(dapot.dict())
    return dapot

@dapot.put('/{id}')
async def dapot_student(id, dapot: Dapot,database=Depends(get_database),curent_user = Depends(get_current_active_user)):
    db_dapot = database["dapot"]
    updated_dapot = await db_dapot.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(dapot)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return DataPotensi(updated_dapot)

@dapot.delete('/{id}')
async def delete_dapot(id,database=Depends(get_database),curent_user = Depends(get_current_active_user)):
    db_dapot = database["dapot"]
    dapot = await db_dapot.find_one_and_delete({"_id": ObjectId(id)})
    if dapot:
        return DataPotensi(dapot)
    else:
        return {"message": "Data Potensi not found"}    
