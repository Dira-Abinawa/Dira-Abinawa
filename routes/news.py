from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.models import News
from config.dbfull import news_connection
from schemas.schemas import NewsPramuka, NewPramuka
from bson import ObjectId
import pymongo

news = APIRouter(tags=["News"])

@news.get('/')
async def find_all_news():
    news_cursor = news_connection.local.news.find()
    news_list = list(news_cursor)
    if not news_list:
        return "Maaf, Anda tidak memiliki data apapun"
    result = [NewPramuka(news) for news in news_list]
    return result


@news.post('/')
async def create_news(news : News):
    news_connection.local.news.insert_one(dict(news))
    return NewsPramuka(news_connection.local.news.find())

@news.put('/{id}')
async def update_news(id, news: News):
    updated_dkr = news_connection.local.news.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(news)},
        return_document=pymongo.ReturnDocument.AFTER
    )
    return NewPramuka(updated_dkr)

@news.delete('/{id}')
async def delete_news(id):
    news = news_connection.local.news.find_one_and_delete({"_id": ObjectId(id)})
    if news:
        return NewPramuka(news)
    else:
        return {"message": "Data not found"}
