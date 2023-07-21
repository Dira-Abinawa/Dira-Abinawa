from fastapi import APIRouter, Request
from config.dbfull import opinion_connection
from schemas.schemas import OpinionPramuka, OpinionsPramuka
from models.models import myOpinion
from bson import ObjectId
import pymongo

opinion = APIRouter(tags=["Opinion"])

@opinion.get('/')
async def find_all_opinion():
    opinion_cursor = opinion_connection.local.opinion.find()
    opinion_list = list(opinion_cursor)
    if not opinion_list:
        return "Maaf, Anda tidak memiliki data apapun"
    result = [OpinionPramuka(opinion) for opinion in opinion_list]
    return result


@opinion.post('/')
async def create_opinion(opinion : myOpinion):
    opinion_connection.local.opinion.insert_one(dict(opinion))
    return OpinionsPramuka(opinion_connection.local.opinion.find())

@opinion.put('/{id}')
async def update_opinion(id, opinion: myOpinion):
    updated_opinion = opinion_connection.local.opinion.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(opinion)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return OpinionPramuka(updated_opinion)

@opinion.delete('/{id}')
async def delete_opinion(id):
    opinion = opinion_connection.local.opinion.find_one_and_delete({"_id": ObjectId(id)})
    if opinion:
        return OpinionPramuka(opinion)
    else:
        return {"message": "Data not found"}
