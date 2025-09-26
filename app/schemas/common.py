# app/schemas/common.py

from datetime import datetime
from pydantic import BaseModel

class Sports(BaseModel):
    """Stores list of sports."""
    id: int
    name: str

class States(BaseModel):
    """Stores list of states."""
    state_id: int
    name: str
    abbreviation: str

    class Config:
        orm_mode = True  # <-- VERY IMPORTANT for SQLAlchemy integration


class Schools(BaseModel):
    """Stores list of schools."""
    school_id: int
    school_name: str

    class Config:
        orm_mode = True  


class Ads(BaseModel):
    """Holds list of advertisement."""
    id: int
    name: str
    headertext: str
    postingdate: datetime
    textfield: str
    navigateurl: str
    imageurl:str
    type: str

    class Config:
        orm_mode = True  


class RecentNews(BaseModel):
    """Hold list of recent news."""
    id :int
    name :str
    header_text :str
    posting_date :datetime
    text_field :str
    navigate_url :str
    image_url :str

    class Config:
        orm_mode = True 

