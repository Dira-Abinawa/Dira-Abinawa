from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from models.models import Dapot
from config.dbfull import db
from routes.login import get_current_active_user, non_admin_required
from schemas.schemas import DataPotensi, DatasPotensi
from bson import ObjectId
import pymongo

dapot = APIRouter(tags=["Data Potensi"])

#get all
@dapot.get('/')
async def find_dapot():
    dapot_cursor = db.dapot.find()
    dapot_list = list(dapot_cursor) 
    return DatasPotensi(dapot_list)

@dapot.post('/')
async def create_dapot(dapot : Dapot,curent_user = Depends(get_current_active_user)):
    db.dapot.insert_one(dict(dapot))
    return DatasPotensi(db.dapot.find())

@dapot.put('/{id}')
async def dapot_student(id, dapot: Dapot,curent_user = Depends(get_current_active_user)):
    updated_dapot = db.dapot.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(dapot)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return DataPotensi(updated_dapot)

@dapot.delete('/{id}')
async def delete_dapot(id,curent_user = Depends(get_current_active_user)):
    dapot = db.dapot.find_one_and_delete({"_id": ObjectId(id)})
    if dapot:
        return DataPotensi(dapot)
    else:
        return {"message": "Data Potensi not found"}    
