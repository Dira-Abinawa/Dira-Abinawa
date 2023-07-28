from fastapi import APIRouter, Request 
from models.models import DKR
from config.dbfull import dkr_connection
from schemas.schemas import DewanKerja, DewansKerja
from bson import ObjectId
import pymongo

dkr = APIRouter(tags=["Dewan Kerja Ranting"])

@dkr.get('/')
async def find_all_dkr():
    dkr_cursor = dkr_connection.local.dkr.find()
    dkr_list = list(dkr_cursor)
    if not dkr_list:
        return "Data not found."

    # Loop through the retrieved documents and set status to "Null" if it's empty or not present
    for dkr in dkr_list:
        for dkr in dkr_list:
            dkr["_id"] = str(dkr["_id"])
            dkr.setdefault("status", False)

    # Create instances of DKR using the updated dkr_list
    result = [DewanKerja(dkr) for dkr in dkr_list]
    return result


@dkr.post('/')
async def create_dkr(dkr : DKR):
    item_data = dkr.dict()
    existing_item = dkr_connection.local.dkr.find_one({"name": item_data["name"]})
    if existing_item:
        return 'Data already exists.'
    else:
        dkr_connection.local.dkr.insert_one(dict(dkr))
        return DewansKerja(dkr_connection.local.dkr.find())

@dkr.put('/{id}')
async def update_dkr(id, dkr: DKR):
    updated_dkr = dkr_connection.local.dkr.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(dkr)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return DewanKerja(updated_dkr)

@dkr.delete('/{id}')
async def delete_dkr(id):
    dkr = dkr_connection.local.dkr.find_one_and_delete({"_id": ObjectId(id)})
    if dkr:
        return DewanKerja(dkr)
    else:
        return {"message": "Data not found"}
