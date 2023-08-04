from pydantic import BaseModel, Field, EmailStr, constr, SecretStr
from enum import Enum
from typing import List, Optional
from config.dbfull import db
from bson import ObjectId
from datetime import datetime

#Users
class UserRegistration(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    hashed_password: str
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str

# Model untuk data token JWT
class TokenData(BaseModel):
    username: str

# Model untuk data pengguna
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    
#Opinion
class myOpinion(BaseModel):
    id: str = Field(alias='_id')
    sender_name : str
    subject : str
    content : str
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
    def __init__(self, **data):
        if '_id' in data and isinstance(data['_id'], ObjectId):
            data['_id'] = str(data['_id'])
        super().__init__(**data)

class Admin(BaseModel):
    full_name: str
    username: str
    email: str
    hashed_password: str
    active: bool
    is_admin : bool

class UserInDB(BaseModel):
    full_name: str
    username: str
    email: str
    hashed_password: str
    active: bool
    is_admin : Optional[bool]
    opinions : List[myOpinion] = []
    
#Activity
class Activity(BaseModel):
    id: str = Field(alias="_id")
    activity_name : str
    circular_letter : str
    participant_requirements : str
    schedule_of_activities : str
    
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, **data):
        if '_id' in data and isinstance(data['_id'], ObjectId):
            data['_id'] = str(data['_id'])
        super().__init__(**data)

#Data Potensi
class Dapot(BaseModel):
    school_name :str
    male_builder : int
    famale_builder : int
    male_member : int
    female_member : int
    bantara_member : int
    laksana_member : int
    garuda_member : int

#Dewan Kerja Ranting
class level(str,Enum):
    def __str__(self):
        return str(self.value)
    BANTARA = "Bantara"
    LAKSANA = "Laksana"
    GARUDA = "Garuda"
    
class DKR(BaseModel):
    name : str
    school_name : str
    level : level
    position : str
    period : str
    status : bool
    
# Comment
class Comments(BaseModel):
    id: str = Field(alias="_id")
    sender_name : str
    content: str
    id_news: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#News
class HashtagParams(str,Enum):
    def __str__(self):
        return str(self.value)
    senang = '#senang'
    bahagia = '#bahagia'
    sedih = '#sedih'
    kecewa = '#kecewa'
    pramuka = '#pramuka'


class News(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    content: Optional[str]
    hashtag: HashtagParams
    thumbnail: Optional[str]
    author : Optional[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    comments: List[Comments] = []

    @classmethod
    def get_comments_by_id_news(cls, news_id):
        # Retrieve comments from MongoDB for the given news_id
        comments_docs = db.comment.find({"id_news": news_id})
        comments = [Comments(**doc) for doc in comments_docs]

        # Retrieve news data from MongoDB
        news_doc = db.news.find_one({"_id": ObjectId(news_id)})

        # Create a News object with the retrieved data and comments
        if news_doc:
            news = cls(
                id=str(news_doc['_id']),  # Convert _id to string and assign it to id
                title=news_doc['title'],
                description=news_doc['description'],
                content=news_doc['content'],
                hashtag=HashtagParams(news_doc['hashtag']),
                thumbnail=news_doc.get('thumbnail'),
                comments=comments
            )
            return news
        else:
            return None

    
#Schools
class School(BaseModel):
    school_name: str = Field(..., max_length=100)
    basis_name: str = Field(..., max_length=100)
    male_ambalan_name: str
    female_ambalan_name: str
    registration_number : bool