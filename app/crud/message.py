# app/crud/message.py
# The message.py module provides all the database logic for the messaging system in the app. It allows users to:
    # * Send, read, mark, delete, and search messages
    # * Query inbox/sent items using a PostgreSQL stored procedure
    # * Track unread messages count for notifications
    # * Update message states like unread, read, replied, or forwarded
    # * It uses a combination of raw SQL stored procedures and SQLAlchemy ORM to interact with the Tbmessages table.

from datetime import datetime
from typing import List, Optional
from pytest import Session
from sqlalchemy import func, text

from app.db.models.sp_db_models import Tbmessages
#from app.db.models.sp_db_models_BK import TbMessages, TbMessagesSent
from app.schemas.message import MessageInfo, SearchMessages

#-----------------------------------------------------------------------------------

def get_messages(db: Session, member_id: int, type:str, show_type: str) -> List[SearchMessages]:
    #Retrieves a list of messages (Inbox or Sent) for a given user.

    sql = text("""SELECT  * FROM public.sp_get_member_messages(:member_id, :type, :show_type) """) # Type=Inbox, Sent; ShowType=All, UnRead
    result = db.execute(sql, {"member_id": member_id, "type": type, "show_type":show_type})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [SearchMessages(**row) for row in rows]

#-----------------------------------------------------------------------------------

def set_send_message(db:Session, data:MessageInfo) -> None:
    # create new message objects
    m = Tbmessages()
    m.sender_id = data.from_
    m.contact_id = data.to
    m.subject = data.subject
    m.msg_date = datetime.utcnow()
    m.body = data.body
    m.attachment = 0
    m.message_state = 0
    m.attachment_file = data.attachment
    m.flag_level = 0
    m.importance_level = 0
    m.original_msg = data.original_msg
    # Add and save
    db.add(m)
    db.commit()

#---------------------------------------------------------------------------------

def set_toggle_message_state (db:Session, status:int, msg_id:int) -> None:
    # Updates the read/unread state of a message.
    if status == 0:  # UnRead
        perform_message_status(0, msg_id, db)
    elif status == 1:  # Read
        perform_message_status(1, msg_id, db)
    elif status == 2:  # Forwarded
        perform_message_status(2, msg_id, db)
    elif status == 3:  # RepliedTo
        perform_message_status(3, msg_id, db)

#------------------------------------------------------------------------

def perform_message_status(status:int, msg_id:int, db):
    # Low-level utility used to update the message_state field of a message.
    msg = db.query(Tbmessages).filter(Tbmessages.message_id == msg_id).first()
    if msg:
        msg.message_state = status
        db.commit()
    else:
        raise ValueError(f"Message with ID {msg_id} not found")

#---------------------------------------------------------------------------------

def set_delete_message(msg_id:int, db:Session) -> None:
    # Permanently deletes a message from the database.
    msg = db.query(Tbmessages).filter(Tbmessages.message_id == msg_id).first()
    if msg:
        db.delete(msg)
        db.commit()
    else:
        raise ValueError(f"Message with ID {msg_id} not found.")
    
#---------------------------------------------------------------------------------
    
def get_total_unread_messages(member_id: int, db: Session ) -> int:
    # Returns the number of unread messages for a member (useful for inbox notifications).
    count = db.query(func.count(Tbmessages.message_id)) \
              .filter(Tbmessages.contact_id == member_id, Tbmessages.message_state == 0) \
              .scalar()
    return count

#---------------------------------------------------------------------------------

def get_message_info(message_id: int, db: Session) -> Optional[MessageInfo]:
    # Retrieves full details of a specific message using stored procedure
    sql = text("""SELECT  * FROM public.sp_get_message_info_by_id(:message_id) """)
    result = db.execute(sql, {"message_id": message_id})
    row = result.mappings().first()
    if row is not None:
        return MessageInfo(**row)
    return None

#---------------------------------------------------------------------------------

def get_searched_messages(member_id: int, db: Session, search_key:str) -> List[SearchMessages]:
    # Searches messages for a member based on a keyword (subject, body, etc.).
    sql = text("""SELECT  * FROM public.sp_search_messages(:member_id, :search_key) """)
    result = db.execute(sql, {"member_id": member_id, "search_key": search_key})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [SearchMessages(**row) for row in rows]