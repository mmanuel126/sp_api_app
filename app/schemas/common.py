# app/schemas/common.py

from datetime import datetime
from pydantic import BaseModel

class Sports(BaseModel):
    """Stores list of sports."""
    id: int
    Name: str

class States(BaseModel):
    """Stores list of states."""
    StateID: int
    Name: str
    Abbreviation: str

    class Config:
        orm_mode = True  # <-- VERY IMPORTANT for SQLAlchemy integration


class Schools(BaseModel):
    """Stores list of schools."""
    SchoolID: int
    SchoolName: str

    class Config:
        orm_mode = True  


class Ads(BaseModel):
    """Holds list of advertisement."""
    ID: int
    Name: str
    HeaderText: str
    PostingDate: datetime
    TextField: str
    NavigateURL: str
    ImageUrl:str
    Type: str

    class Config:
        orm_mode = True  


class RecentNews(BaseModel):
    """Hold list of recent news."""
    ID :int
    Name :str
    HeaderText :str
    PostingDate :datetime
    TextField :str
    NavigateURL :str
    ImageUrl :str

    class Config:
        orm_mode = True 

