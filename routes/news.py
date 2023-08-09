from fastapi import APIRouter, Request, HTTPException, Query, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from models.models import News, HashtagParams, Comments, UserInDB
from config.dbfull import get_database
from schemas.schemas import NewsPramuka, NewPramuka
from routes.comment import get_comment_by_id
from bson import ObjectId
import pymongo
from pymongo import DESCENDING
from routes.login import get_current_active_user
from typing import Optional, List
from datetime import datetime

news = APIRouter(tags=["News"])

@news.get('/')
async def find_all_news(database=Depends(get_database)):
    news_db = database["news"]
    news_cursor = news_db.find()
    news_list = await news_cursor.to_list(length=None)
    if not news_list:
        return []
    result_news = []

    for news_item in news_list:
        news_id = str(news_item["_id"])
        query = {"id_news": news_id}
        comment_db = database["comment"]
        comment_cursor = comment_db.find(query)
        comments_data = await comment_cursor.to_list(length=None)
        comments = [Comments(**{**comment, "_id": str(comment["_id"])}) for comment in comments_data]
        updated_at = news_item.get("updated_at")
        author = news_item.get("author", "Unknown")
        result_news.append(News(
            id=news_id,
            title=news_item["title"],
            description=news_item["description"],
            content=news_item["content"],
            hashtag=HashtagParams(news_item["hashtag"]),
            thumbnail=news_item["thumbnail"],
            author=author,
            created_at=news_item.get("created_at"),
            updated_at=updated_at,
            comments=comments
        ))

    return result_news
   
@news.post('/')
async def create_news(
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    hashtag: str = Form(...),
    thumbnail: str = Form(...),
    current_user: UserInDB = Depends(get_current_active_user),
    database = Depends(get_database)
):
    news_db = database["news"]
    existing_item = await news_db.find_one({"title": title})
    if existing_item:
        raise HTTPException(status_code=400, detail="Data already exists.")
    else:
        new_news_data = {
            "title": title,
            "description": description,
            "content": content,
            "hashtag": hashtag,
            "thumbnail": thumbnail,
            "author": current_user.full_name,
            "created_at": datetime.utcnow(),
        }
        result = await news_db.insert_one(new_news_data)
        new_news_data["_id"] = str(result.inserted_id)
        return new_news_data
    
@news.get('/hashtag')
async def get_by_hashtag(database = Depends(get_database), hashtag: Optional[str] = Query(None, enum=[item.value for item in HashtagParams])):
    news_db = database["news"]
    comment_db = database["comment"]

    filter_params = {}
    if hashtag and hashtag in [item.value for item in HashtagParams]:
        filter_params["hashtag"] = hashtag

    existing_items = news_db.find(filter_params)
    result_filter = await existing_items.to_list(None)

    if not result_filter:
        raise HTTPException(status_code=404, detail="Data not found")

    for news_item in result_filter:
        news_id = str(news_item["_id"]) 
        comment_cursor = comment_db.find({"id_news": news_id})
        comments = await parse_comments(comment_cursor)
        news_item["_id"] = str(news_item["_id"]) 
        news_item["comments"] = comments

    return jsonable_encoder(result_filter)

async def parse_comments(comment_cursor):
    comments = []
    async for comment in comment_cursor:
        comment_dict = comment.copy()
        comment_dict["_id"] = str(comment["_id"]) 
        comments.append(comment_dict)
    return comments

@news.put('/{id}')
async def update_news(
    id: str,
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    hashtag: str = Form(...),
    thumbnail: str = Form(...),
    current_user= Depends(get_current_active_user),
    database=Depends(get_database),
):
    news_db = database["news"]
    news_data = {
        "title": title,
        "description": description,
        "content": content,
        "hashtag": hashtag,
        "thumbnail": thumbnail,
        "updated_at": datetime.now()
    }
    if current_user.is_admin:
        updated_news = await news_db.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": news_data},
            return_document=pymongo.ReturnDocument.AFTER
        )
    else:
        existing_news = await news_db.find_one({"_id": ObjectId(id), "author": current_user.full_name})
        if not existing_news:
            raise HTTPException(status_code=403, detail="You are not allowed to edit this news.")
        updated_news = await news_db.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": news_data},
            return_document=pymongo.ReturnDocument.AFTER
        )
    if not updated_news:
        raise HTTPException(status_code=404, detail="News not found.")
    return HTTPException(status_code=200, detail=NewPramuka(updated_news), headers="Data added successfully!")

@news.delete('/{id}')
async def delete_news(
    id: str,
    curent_user: UserInDB = Depends(get_current_active_user),
    database=Depends(get_database)
):
    is_admin = curent_user.is_admin
    news_db = database["news"]
    news_data = await news_db.find_one({"_id":ObjectId(id)})
    if news_data:
        if is_admin or news_data["author"] == curent_user.full_name:
            await news_db.find_one_and_delete({"_id": ObjectId(id)})
            return {"message": "News deleted successfully"}
        else:
            return {"message": "You are not authorized to delete this news."}
    else:
        raise HTTPException(status_code=404, detail="Data not found")
