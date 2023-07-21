from pydantic import BaseModel
from enum import Enum

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