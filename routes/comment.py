from fastapi import APIRouter, Request, Query, HTTPException
from config.dbfull import coment_connection
from schemas.schemas import NewsComentItem, NewsComents
from models.models import Comments
from bson import ObjectId
import pymongo

comment = APIRouter(tags=["Comments"])

@comment.get('/')
async def find_all_comment():
    coment_cursor = coment_connection.local.coment.find()
    coment_list = list(coment_cursor)
    if not coment_list:
        return "Data not found."

    result = []
    for coment in coment_list:
        if "id_news" not in coment:
            # If "id_news" key is missing, you can choose to skip this comment or handle it accordingly
            continue

        comment_item = NewsComentItem(coment)
        result.append(comment_item)

    return result

@comment.get('/by_news/{id_news}')
async def get_comment_by_id(id_news: str):
    comment_cursor = coment_connection.local.coment.find({"id_news": id_news})
    comment_list = list(comment_cursor)
    
    if not comment_list:
        raise HTTPException(status_code=404, detail="Data not found")

    for comment in comment_list:
        comment["_id"] = str(comment["_id"])

    return comment_list



@comment.post('/')
async def create_comment(opinion : Comments):
    coment_connection.local.coment.insert_one(dict(opinion))
    return NewsComents(coment_connection.local.coment.find())

@comment.put('/{id}')
async def update_comment(id, opinion: Comments):
    updated_comment = coment_connection.local.coment.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(opinion)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return NewsComentItem(updated_comment)

@comment.delete('/{id}')
async def delete_comment(id):
    opinion = coment_connection.local.coment.find_one_and_delete({"_id": ObjectId(id)})
    if opinion:
        return NewsComentItem(opinion)
    else:
        return {"message": "Data not found"}
