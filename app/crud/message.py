# app/crud/message.py

from datetime import datetime
from typing import List, Optional
from pytest import Session
from sqlalchemy import func, text

from app.db.models.sp_db_models import TbMessages, TbMessagesSent
from app.schemas.message import MessageInfo, SearchMessages

#-----------------------------------------------------------------------------------

def get_messages(db: Session, member_id: int, type:str, showType: str) -> List[SearchMessages]:
    sql = text("EXEC spGetMemberMessages :MemberID, :Type, :ShowType") # Type=Inbox, Sent; ShowType=All, UnRead
    result = db.execute(sql, {"MemberID": member_id, "Type": type, "ShowType":showType})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [SearchMessages(**row) for row in rows]

#-----------------------------------------------------------------------------------

def set_send_message(db:Session, data:MessageInfo) -> None:
    # create new message objects
    m = TbMessages()
    ms = TbMessagesSent()

    m.SenderID = data.From
    ms.SenderID = data.From

    m.ContactID = data.To
    ms.ContactID = data.To

    m.Subject = data.Subject
    ms.Subject = data.Subject

    m.MsgDate = datetime.utcnow()
    ms.MsgDate = datetime.utcnow()

    m.Body = data.Body
    ms.Body = data.Body

    has_attachment = bool(data.Attachment)
    m.Attachment = has_attachment
    ms.Attachment = has_attachment

    m.MessageState = 0
    ms.MessageState = 0

    m.AttachmentFile = data.Attachment
    ms.AttachmentFile = data.Attachment

    m.FlagLevel = 0
    ms.FlagLevel = 0

    m.ImportanceLevel = 0
    ms.ImportanceLevel = 0

    m.OriginalMsg = data.OriginalMsg
    ms.OriginalMsg = data.OriginalMsg

    # Add and save
    db.add(m)
    db.add(ms)
    db.commit()

#---------------------------------------------------------------------------------

def set_toggle_message_state (db:Session, status:int, msg_id:int) -> None:
    if status == 0:  # UnRead
        perform_message_status(0, msg_id, db)
    elif status == 1:  # Read
        perform_message_status(1, msg_id, db)
    elif status == 2:  # Forwarded
        perform_message_status(2, msg_id, db)
    elif status == 3:  # RepliedTo
        perform_message_status(3, msg_id, db)

def perform_message_status(status:int, msg_id:int, db):
    msg = db.query(TbMessages).filter(TbMessages.MessageID == msg_id).first()
    if msg:
        msg.MessageState = status
        db.commit()
    else:
        raise ValueError(f"Message with ID {msg_id} not found")

#---------------------------------------------------------------------------------

def set_delete_message(msg_id:int, db:Session) -> None:
    msg = db.query(TbMessages).filter(TbMessages.MessageID == msg_id).first()
    if msg:
        db.delete(msg)
        db.commit()
    else:
        raise ValueError(f"Message with ID {msg_id} not found.")
    
#---------------------------------------------------------------------------------
    
def get_total_unread_messages(member_id: int, db: Session ) -> int:
    count = db.query(func.count(TbMessages.MessageID)) \
              .filter(TbMessages.ContactID == member_id, TbMessages.MessageState == 0) \
              .scalar()
    return count

#---------------------------------------------------------------------------------

def get_message_info(message_id: int, db: Session) -> Optional[MessageInfo]:
    sql = text("EXEC spGetMessageInfoByID :MsgID") 
    result = db.execute(sql, {"MsgID": message_id})
    row = result.mappings().first()
    if row is not None:
        return MessageInfo(**row)
    return None

#---------------------------------------------------------------------------------

def get_searched_messages(member_id: int, db: Session, search_key:str) -> List[SearchMessages]:
    sql = text("EXEC spSearchMessages :MemberID, :SearchKey") 
    result = db.execute(sql, {"MemberID": member_id, "SearchKey": search_key})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [SearchMessages(**row) for row in rows]