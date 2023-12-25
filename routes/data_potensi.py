from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from models.models import Dapot, School, UserInDB
from config.dbfull import get_database
from routes.login import get_current_active_user, get_current_user, non_admin_required
from schemas.schemas import DataPotensi, DatasPotensi
from bson import ObjectId
from pymongo.collection import Collection
import pymongo

dapot = APIRouter(tags=["Data Potensi"])

@dapot.get('/')
async def find_dapot(
        current_user: UserInDB = Depends(get_current_user),
    database: Collection = Depends(get_database)
):
    # Retrieve dapot details for the current user
    db_dapot = database["dapot"]
    dapot = await db_dapot.find_one({"gudep": current_user.gudep_number})

    if not dapot:
        raise HTTPException(status_code=404, detail="Dapot not found")

    # Retrieve schools associated with the user's gudep number
    db_school = database["schools"]
    gudep_cursor = db_school.find({"gudep": current_user.gudep_number})

    schools = []
    async for school in gudep_cursor:
        # Convert ObjectId to string
        if "_id" in school:
            school["_id"] = str(school["_id"])
        schools.append(school)

    # Prepare dapot details with opinions and school information
    dapot_with_opinions = {
        "school": schools,
        "male_builder": dapot.get("male_builder", 0),
        "female_builder": dapot.get("female_builder", 0),
        "male_member": dapot.get("male_member", 0),
        "female_member": dapot.get("female_member", 0),
        "bantara_member": dapot.get("bantara_member", 0),
        "laksana_member": dapot.get("laksana_member", 0),
        "garuda_member": dapot.get("garuda_member", 0)
    }

    return JSONResponse(dapot_with_opinions)

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
