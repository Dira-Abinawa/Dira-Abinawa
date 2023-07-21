from pydantic import BaseModel
    
class News(BaseModel):
    title : str
    description : str
    content : str
    thumbnail : str