from pydantic import BaseModel,Field

class School(BaseModel):
    school_name: str = Field(..., max_length=100)
    basis_name: str = Field(..., max_length=100)
    male_ambalan_name: str
    female_ambalan_name: str