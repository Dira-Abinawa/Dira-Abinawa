from fastapi import APIRouter, Request, HTTPException, Query, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from models.models import News, HashtagParams, Comments, UserInDB
from config.dbfull import news_connection, coment_connection,db    
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
async def find_all_news():
    news_cursor = news_connection.local.news.find()
    news_list = list(news_cursor)
    if not news_list:
        return "Data not found."
    result_news = []
    result_comment = []

    for news_item in news_list:
        news_id = str(news_item["_id"])
        
        query = {"id_news": news_id}
        comment_cursor = coment_connection.local.coment.find(query)
        comments = [Comments(**comment)for comment in comment_cursor]
        
        updated_at = news_item.get("updated_at")
        if comments:
            result_news.append(News(
                id=news_id,
                title=news_item["title"],
                description=news_item["description"],
                content=news_item["content"],
                hashtag=HashtagParams(news_item["hashtag"]),
                thumbnail=news_item["thumbnail"],
                created_at=news_item.get("created_at"),
                updated_at_at=updated_at,
                comments=comments
            ))
        else:
            result_news.append(News(
                id=news_id,
                title=news_item["title"],
                description=news_item["description"],
                content=news_item["content"],
                hashtag=HashtagParams(news_item["hashtag"]),
                thumbnail=news_item["thumbnail"],
                created_at=news_item.get("created_at"),
                updated_at=updated_at if updated_at is not None else None,
            ))
    return result_news    

@news.post('/')
async def create_news(
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    hashtag: str = Form(...),
    thumbnail: str = Form(...),
    current_user: UserInDB = Depends(get_current_active_user)
):
    existing_item = news_connection.local.news.find_one({"title": title})
    if existing_item:
        raise HTTPException(status_code=400, detail="Data already exists.")
    else:
        new_news_data = {
            "title": title,
            "description": description,
            "content": content,
            "hashtag": hashtag,
            "thumbnail": thumbnail,
            "created_at": datetime.utcnow(),
        }
        news_connection.local.news.insert_one(new_news_data)
        return NewsPramuka(news_connection.local.news.find())
    
@news.get('/hashtag')
async def get_by_hashtag(hashtag: str = Query(
        None,
        enum=[item.value for item in HashtagParams],
    )):
    if hashtag and hashtag in [item.value for item in HashtagParams]:
        existing_item = news_connection.local.news.find({"hashtag": hashtag})
    else:
        existing_item = news_connection.local.news.find({"hashtag": hashtag})
    result_filter = list(existing_item)
    if not result_filter:
        raise HTTPException(status_code=404, detail="Data not found")

    # Loop through the filtered news items and fetch comments for each news item
    for news_item in result_filter:
        news_id = str(news_item["_id"])  # Convert _id to string to use in the query
        # Query to find comments with the same id_news as the news item
        comment_cursor = coment_connection.local.coment.find({"id_news": news_id})
        comments = [Comments(**comment).dict(exclude={"id_news"}) for comment in comment_cursor]
        news_item["comments"] = comments

    # Manually handle serialization of ObjectId to string
    for item in result_filter:
        item["_id"] = str(item["_id"])

    # Use jsonable_encoder after manually handling ObjectId serialization
    return jsonable_encoder(result_filter)

@news.put('/{id}')
async def update_news(
    id: str,
    title: str = Form(...),
    description: str = Form(...),
    content: str = Form(...),
    hashtag: str = Form(...),
    thumbnail: str = Form(...),
    created_at: str = Form(...),
):
    # Konversi data ke dalam bentuk dict yang sesuai dengan struktur News model
    news_data = {
        "title": title,
        "description": description,
        "content": content,
        "hashtag": hashtag,
        "thumbnail": thumbnail,
        "created_at": created_at,
        "updated_at":datetime.now()
    }

    updated_news = news_connection.local.news.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": news_data},
        return_document=pymongo.ReturnDocument.AFTER
    )

    return NewPramuka(updated_news)

@news.delete('/{id}')
async def delete_news(id):
    news = news_connection.local.news.find_one_and_delete({"_id": ObjectId(id)})
    if news:
        return NewPramuka(news)
    else:
        return {"message": "Data not found"}
