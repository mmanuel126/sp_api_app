# app/schemas/message.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Messages (BaseModel):
    """Holds the log in data."""
    MessageID  : Optional[str] = None 
    SentDate  : Optional[str] = None 
    From  : Optional[str] = None 
    SenderPicture  : Optional[str] = None 
    Body  : Optional[str] = None 
    Subject  : Optional[str] = None 
    AttachmentFile  : Optional[str] = None 
    OrginalMsg  : Optional[str] = None 
    

class SearchMessages (BaseModel):
    """Stores message info."""
    Attachment  : Optional[bool] = None 
    Body  : Optional[str] = None 
    ContactName  : Optional[str] = None 
    ContactImage  : Optional[str] = None 
    SenderImage  : Optional[str] = None 
    ContactID  : Optional[int] = None 
    FlagLevel  : Optional[int] = None 
    ImportanceLevel  : Optional[int] = None 
    MessageID  : Optional[int] = None 
    MessageState  : Optional[int] = None 
    SenderID  : Optional[str] = None 
    Subject  : Optional[str] = None 
    MsgDate  : Optional[datetime] = None 
    FromID  : Optional[int] = None 
    FirstName  : Optional[str] = None 
    FullBody  : Optional[str] = None 
    SenderTitle : Optional[str] = None 
    
class MessageInfo (BaseModel):
    """Holds the message info."""
    To : Optional[str] = None 
    From : Optional[str] = None 
    Subject : Optional[str] = None 
    Body : Optional[str] = None 
    Attachment : Optional[str] = None 
    OriginalMsg : Optional[str] = None 
    MessageID : Optional[int] = None 
    SentDate : Optional[datetime] = None 
    SenderPicture: Optional[str] = None 


    

    