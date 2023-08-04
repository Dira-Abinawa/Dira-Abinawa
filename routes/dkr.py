from fastapi import APIRouter, Request, Depends
from models.models import DKR
from config.dbfull import db
from routes.login import admin_required
from schemas.schemas import DewanKerja, DewansKerja
from bson import ObjectId
import pymongo

dkr = APIRouter(tags=["Dewan Kerja Ranting"])

@dkr.get('/')
async def find_all_dkr():
    dkr_cursor = db.dkr.find()
    dkr_list = list(dkr_cursor)
    if not dkr_list:
        return "Data not found."
    for dkr in dkr_list:
        for dkr in dkr_list:
            dkr["_id"] = str(dkr["_id"])
            dkr.setdefault("status", False)
    result = [DewanKerja(dkr) for dkr in dkr_list]
    return result

@dkr.post('/',dependencies=[Depends(admin_required)])
async def create_dkr(dkr : DKR):
    existing_item = db.dkr.find_one({"name": dkr.name})
    if existing_item:
        return 'Data already exists.'
    else:
        db.dkr.insert_one(dict(dkr))
        return DewansKerja(db.dkr.find())

@dkr.put('/{id}',dependencies=[Depends(admin_required)])
async def update_dkr(id, dkr: DKR):
    updated_dkr = db.dkr.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(dkr)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return DewanKerja(updated_dkr)

@dkr.delete('/{id}',dependencies=[Depends(admin_required)])
async def delete_dkr(id):
    dkr = db.dkr.find_one_and_delete({"_id": ObjectId(id)})
    if dkr:
        return DewanKerja(dkr)
    else:
        return {"message": "Data not found"}
