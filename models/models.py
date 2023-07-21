from pydantic import BaseModel, Field
from enum import Enum

class Activity(BaseModel):
    activity_name : str
    circular_letter : str
    participant_requirements : str
    schedule_of_activities : str
    
class Dapot(BaseModel):
    school_name :str
    male_builder : int
    famale_builder : int
    male_member : int
    female_member : int
    bantara_member : int
    laksana_member : int
    garuda_member : int

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
    
class News(BaseModel):
    title : str
    description : str
    content : str
    thumbnail : str
    
class myOpinion(BaseModel):
    sender_name : str
    subject : str
    content : str
    
class School(BaseModel):
    school_name: str = Field(..., max_length=100)
    basis_name: str = Field(..., max_length=100)
    male_ambalan_name: str
    female_ambalan_name: str