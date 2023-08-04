from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument
from config.dbfull import get_database
from routes.login import get_current_active_user
from schemas.schemas import ActivityPramuka
from models.models import Activity
from bson import ObjectId
from config.dbfull import get_database
from pymongo.errors import DuplicateKeyError

activity = APIRouter(tags=["Activity"])

@activity.get('/')
async def find_all_activity(database=Depends(get_database)):
    activity_collection = database['activity']
    activity_cursor = activity_collection.find()
    activity_list = await activity_cursor.to_list(length=None)
    
    result = [Activity(**activity) for activity in activity_list]
    return result

@activity.post('/')
async def create_activity(activity: Activity, database=Depends(get_current_active_user)):
    activity_collection = database['activity']
    try:
        result = await activity_collection.insert_one(activity.dict())
        activity_id = str(result.inserted_id)
        return {"message": "Data added successfully!", "activity_id": activity_id}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Duplicate activity name")

@activity.put('/{id}')
async def update_activity(id: str, activity: Activity, database=Depends(get_current_active_user)):
    activity_collection = database['activity']
    activity_id = ObjectId(id)
    updated_activity = await activity_collection.find_one_and_update(
        {"_id": activity_id},
        {"$set": activity.dict()},
        return_document=ReturnDocument.AFTER
    )
    if updated_activity:
        return {"message": "Data updated successfully!", "activity_id": str(updated_activity["_id"])}
    else:
        raise HTTPException(status_code=404, detail="Data not found")

@activity.delete('/{id}')
async def delete_activity(id: str, database=Depends(get_current_active_user)):
    activity_collection = database['activity']
    activity_id = ObjectId(id)
    delete_result = await activity_collection.delete_one({"_id": activity_id})
    if delete_result.deleted_count == 1:
        return {"message": "Data deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Data not found")