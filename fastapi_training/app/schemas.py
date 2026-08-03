from pydantic import BaseModel,EmailStr,Field 
from typing import Optional

class StudentCreate(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    age:int=Field(ge=16,le=60)
    marks:float=Field(ge=0,le=100)
    password:str
    scholarship:float
    active:bool

class ResponseModel(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    marks: float

# patch model
class StudentUpdate(BaseModel):
    name:Optional[str]=Field(default=None,min_length=2,max_length=100)
    email:Optional[EmailStr]=None
    age:Optional[int]=None
    marks:Optional[float]=Field(default=None,ge=0,le=100)
    password:Optional[float]=None
    scholarship:Optional[float]=None