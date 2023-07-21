from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from models.models import Activity
from config.dbfull import activity_connection
from schemas.schemas import ActivityPramuka, ActivitiesPramuka
from bson import ObjectId
import pymongo

activity = APIRouter(tags=["Activity"])

@activity.get('/')
async def find_all_activity():
    activity_cursor = activity_connection.local.activity.find()
    activity_list = list(activity_cursor)
    if not activity_list:
        return "Maaf, Anda tidak memiliki data apapun"
    result = [ActivityPramuka(activity) for activity in activity_list]
    return result

@activity.post('/')
async def create_activity(activity: Activity):
    activity_connection.local.activity.insert_one(dict(activity))
    return ActivitiesPramuka(activity_connection.local.activity.find())

@activity.put('/{id}')
async def activity_student(id, activity: Activity):
    updated_activity = activity_connection.local.activity.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(activity)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return ActivityPramuka(updated_activity)

@activity.delete('/{id}')
async def delete_activity(id):
    activity = activity_connection.local.activity.find_one_and_delete({"_id": ObjectId(id)})
    if activity:
        return ActivityPramuka(activity)
    else:
        return {"message": "Data not found"}