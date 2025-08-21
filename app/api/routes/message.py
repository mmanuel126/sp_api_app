# app/api/routes/message.py 

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pytest import Session

from app.auth.dependencies import get_current_user
#from app.crud.contact import set_send_request
from app.crud.message import get_message_info, get_messages, get_searched_messages, get_total_unread_messages, set_delete_message, set_send_message, set_toggle_message_state
from app.db.session import get_db
from app.schemas.message import MessageInfo, SearchMessages

router = APIRouter(prefix="/message", tags=["Message"])

#-----------------------------------------------------------------------------------

@router.get("/messages",response_model=List[SearchMessages],
    summary="Returns list of member's messages.",
    description="This endpoint returns the list of messages given a member id."
)
def search_results(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...), type:str  = Query(...), show_type:str  = Query(...)):
    try:
        st = get_messages(db, member_id, type, show_type)
        if not st:
            raise HTTPException(status_code=404, detail="Messages not found.")
        return st
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/send-message",
    summary="Create and send a message given msg info.",
    description="Given message info this endpoint send the msg to a member."
)
def send_message(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  data: MessageInfo = Body(...)
                  ):
    try:
        set_send_message(db, data)
        return {"message": "Sent message successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.put("/toggle-message-state",
    summary="Toggles the state of the message.",
    description="Toggles the state of the message, i.e., read or un-read."
)
def toggle_message_state(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  status: int = Query(...),
                  msgID: int = Query(...)
                  ):
    try:
        set_toggle_message_state(db, status, msgID)
        return {"message": "Toggle message state successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.delete("/delete/{message_id}",
    summary="Deletes the message id.",
    description="This endpoint deletes a given message id."
)
def delete_message(message_id:int, db: Session = Depends(get_db),
        current_user: str = Depends(get_current_user)
    ):
    try:
        set_delete_message(message_id, db)
        return {"message": "Delete message successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.get("/total-unread-messages/{member_id}",response_model=int,
    summary="Gets the total unread messages.",
    description="This endpoint returns the total number of unread messages."
)
def total_unread_messages(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        total = get_total_unread_messages(member_id, db )
        if not total:
            raise HTTPException(status_code=404, detail="total unread messages count not found.")
        return total
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/message-info/{message_id}",response_model=MessageInfo,
    summary="Returns a message info.",
    description="This endpoint returns a message info given a message id."
)
def message_info(message_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        msginfo = get_message_info(message_id, db)
        if not msginfo:
            raise HTTPException(status_code=404, detail="Message info not found.")
        return msginfo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/search-messages/{member_id}",response_model=List[SearchMessages],
    summary="Returns list of member's searched messages.",
    description="This endpoint returns the list of member's searched messages."
)
def search_results(member_id: int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user), search_key:str  = Query(...)):
    try:
        sm = get_searched_messages(member_id, db, search_key)
        if not sm:
            raise HTTPException(status_code=404, detail="Searched messages not found.")
        return sm
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))