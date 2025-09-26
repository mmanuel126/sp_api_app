# app/schemas/message.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Messages (BaseModel):
    """Holds the log in data."""
    message_id  : Optional[str] = None 
    sent_date  : Optional[str] = None 
    from_: Optional[str] = Field(None, alias='from') 
    sender_picture  : Optional[str] = None 
    body  : Optional[str] = None 
    subject  : Optional[str] = None 
    attachment_file  : Optional[str] = None 
    original_msg  : Optional[str] = None 
    

class SearchMessages (BaseModel):
    """Stores message info."""
    attachment  : Optional[bool] = None 
    body  : Optional[str] = None 
    contact_name  : Optional[str] = None 
    contact_image  : Optional[str] = None 
    sender_image  : Optional[str] = None 
    contact_id  : Optional[int] = None 
    flag_level  : Optional[int] = None 
    importance_level  : Optional[int] = None 
    message_id  : Optional[int] = None 
    message_state  : Optional[int] = None 
    sender_id  : Optional[str] = None 
    subject  : Optional[str] = None 
    msg_date  : Optional[datetime] = None 
    from_id  : Optional[int] = None 
    first_name  : Optional[str] = None 
    full_body  : Optional[str] = None 
    sender_title : Optional[str] = None 
    
class MessageInfo (BaseModel):
    """Holds the message info."""
    to : Optional[str] = None 
    from_: Optional[str] = Field(None, alias='from')
    subject : Optional[str] = None 
    body : Optional[str] = None 
    attachment : Optional[int] = None 
    original_msg : Optional[str] = None 
    message_id : Optional[int] = None 
    sent_date : Optional[datetime] = None 
    sender_picture: Optional[str] = None 


    

    