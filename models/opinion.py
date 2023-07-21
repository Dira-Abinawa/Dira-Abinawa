from pydantic import BaseModel

class myOpinion(BaseModel):
    sender_name : str
    subject : str
    content : str