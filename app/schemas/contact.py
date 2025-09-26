# app/schemas/contact.py

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Search(BaseModel):
    """Holds searched contact info."""
    entity_id: int
    entity_name: Optional[str] = None
    picture_path: Optional[str] = None
    location: Optional[str] = None
    event_date: Optional[datetime] = None
    rsvp: Optional[str] = None
    params: Optional[str] = None
    description: Optional[str] = None
    member_count: Optional[str] = None
    created_date: Optional[datetime] = None
    city_state: Optional[str] = None
    email: Optional[str] = None
    name_and_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    label_text: Optional[str] = None
    show_cancel: Optional[str] = None
    paramsav: Optional[str] = None
    stype: Optional[str] = None  

    class Config:
        orm_mode = True


class MemberContacts(BaseModel):
       """Stores member contacts info."""
       friend_name: Optional[str] = None 
       first_name: Optional[str] = None 
       location: Optional[str] = None 
       picture_path: Optional[str] = None 
       contact_id: Optional[int] = None 
       show_type: Optional[str] = None 
       status: Optional[str] = None 
       title_desc: Optional[str] = None 
       params: Optional[str] = None 
       paramsav: Optional[str] = None 
       email: Optional[str] = None 
       label_text: Optional[str] = None 
       Name_and_id: Optional[str] = None 
       show_follow: Optional[str] = None 
    
       class Config:
        orm_mode = True