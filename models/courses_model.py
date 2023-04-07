from bson.objectid import ObjectId
from typing import List
from pydantic import BaseModel

class Chapter(BaseModel):
    _id: ObjectId = None
    name: str
    text: str
    positive_rating: int = 0
    negative_rating: int = 0

    class Config:
        orm_mode = True

class Course(BaseModel):
    _id: ObjectId = None
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]
    total_positive_ratings: int = 0
    total_negative_ratings: int = 0


    class Config:
        orm_mode = True