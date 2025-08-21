# app/schemas/contact.py

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Search(BaseModel):
    """Holds searched contact info."""
    EntityID: int
    EntityName: Optional[str] = None
    PicturePath: Optional[str] = None
    Location: Optional[str] = None
    EventDate: Optional[datetime] = None
    Rsvp: Optional[str] = None
    Params: Optional[str] = None
    Description: Optional[str] = None
    MemberCount: Optional[str] = None
    CreatedDate: Optional[datetime] = None
    CityState: Optional[str] = None
    Email: Optional[str] = None
    NameAndID: Optional[str] = None
    StartDate: Optional[datetime] = None
    EndDate: Optional[datetime] = None
    LabelText: Optional[str] = None
    ShowCancel: Optional[str] = None
    ParamsAV: Optional[str] = None
    Stype: Optional[str] = None  

    class Config:
        orm_mode = True


class MemberContacts(BaseModel):
       """Stores member contacts info."""
       FriendName: Optional[str] = None 
       FirstName: Optional[str] = None 
       Location: Optional[str] = None 
       PicturePath: Optional[str] = None 
       ContactID: Optional[int] = None 
       ShowType: Optional[str] = None 
       Status: Optional[int] = None 
       TitleDesc: Optional[str] = None 
       Params: Optional[str] = None 
       ParamsAV: Optional[str] = None 
       Email: Optional[str] = None 
       LabelText: Optional[str] = None 
       NameAndID: Optional[str] = None 
       ShowFollow: Optional[str] = None 
    
       class Config:
        orm_mode = True