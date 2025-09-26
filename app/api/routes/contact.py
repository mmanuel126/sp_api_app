# app/api/routes/contact.py - social networking app contact related endpoints

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pytest import Session

from app.auth.dependencies import get_current_user
from app.crud.contact import get_member_contacts, get_member_requests, get_member_suggestions, get_people_iam_following, get_search_contacts, get_search_results, get_searched_member_contacts, get_whose_following_me, set_accept_request, set_delete_contact, set_follow_member, set_reject_request, set_send_request, set_unfollow_member
from app.db.session import get_db
from app.schemas.contact import MemberContacts, Search

router = APIRouter(prefix="/contact", tags=["Contact"])

#---------------------------------contact search query --------------------------------------------------

@router.get("/search-results",response_model=List[Search],
    summary="returns list of contacts by search text",
    description="This endpoint returns the list of contacts given a search text."
)
def search_results(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...), search_text:str  = Query(...)):
    try:
        st = get_search_results(db, member_id, search_text)
        if not st:
            raise HTTPException(status_code=404, detail="Search results not found.")
        return st
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#------------------------------------list of members user is following-----------------------------------------------

@router.get("/people-iam-following",response_model=List[MemberContacts],
    summary="returns list of people i follow.",
    description="This endpoint returns a list of site members i follow."
)
def people_iam_following(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...)):
    try:
        result = get_people_iam_following(db, member_id)
        if not result:
            raise HTTPException(status_code=404, detail="No followed members found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#----------------------------------list of members whose following the user-------------------------------------------------

@router.get("/whose-following-me",response_model=List[MemberContacts],
    summary="returns list of people following me.",
    description="This endpoint returns a list of members following me."
)
def whose_following_me(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...)):
    try:
        result = get_whose_following_me(db, member_id)
        if not result:
            raise HTTPException(status_code=404, detail="No members following me found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#----------------------------------post to follow a member-------------------------------------------------

@router.post("/follow-member",
    summary="post to follow member given member id and contact id.",
    description="Given member id and contact id this endpoint sets up member to follow contact."
)
def follow_member(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        set_follow_member(db, member_id, contact_id)
        return {"message": "Member followed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#--------------------------------post to unfollow member---------------------------------------------------

@router.post("/unfollow-member",
    summary="post to un-follow member given member id and contact id.",
    description="Given member id and contact id this endpoint sets up member to un-follow contact."
)
def unfollow_member(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        set_unfollow_member(db, member_id, contact_id)
        return {"message": "Member Unfollowed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#----------------------------------post send a contact request-------------------------------------------------

@router.post("/send-request",
    summary="post to send request given member id and contact id.",
    description="Given member id and contact id this endpoint send request to contact."
)
def send_request(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        msg = "I would like to add you to my contact list so we can start networking. Please accept the request from your request connections list."
        set_send_request(db, member_id, contact_id,msg)
        return {"message": "Send request successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------list of contacts------------------------------------------------

@router.get("/contacts",response_model=List[MemberContacts],
    summary="returns list of them member's contacts.",
    description="This endpoint returns a list of the member's contacts."
)
def contacts(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...)):
    try:
        result = get_member_contacts(db, member_id)
        if not result:
            raise HTTPException(status_code=404, detail="No member's contacts found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#----------------------------------search member contacts-------------------------------------------------

@router.get("/search-member-contacts",response_model=List[MemberContacts],
    summary="returns list of the member's searched contacts.",
    description="This endpoint returns a list of the member's searched contacts base on givent text."
)
def search_member_contacts(db: Session = Depends(get_db),
             current_user: str = Depends(get_current_user), 
             member_id:int = Query(...),
             search_text:str = Query(...)):
    try:
        result = get_searched_member_contacts(db, member_id, search_text)
        if not result:
            raise HTTPException(status_code=404, detail="No member's contacts found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#--------------------------------------remove a user's contact---------------------------------------------

@router.delete("/delete-contact",
    summary="remove a contact from a member's contact list.",
    description="Given member id and contact id this endpoint removes a contact's from his/hers contacts list."
)
def delete_contact(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        set_delete_contact(db, member_id, contact_id)
        return {"message": "Delete contact successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#------------------------------------accept a member request for contact-----------------------------------------------

@router.post("/accept-request",
    summary="accepst request from contact id.",
    description="Given member id and contact id this endpoint sets up member to accepts contact."
)
def accept_request(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        set_accept_request(db, member_id, contact_id)
        return {"message": "Accept request successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#---------------------------------------reject a member request for contact--------------------------------------------

@router.post("/reject-request",
    summary="reject request from a contact id.",
    description="Given member id and contact id this endpoint sets up to reject the request by contact id."
)
def reject_request(db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  member_id:int = Query(...),
                  contact_id:int = Query(...)):
    try:
        set_reject_request(db, member_id, contact_id)
        return {"message": "Reject request successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#---------------------------------------list of requests for contact--------------------------------------------

@router.get("/requests",response_model=List[MemberContacts],
    summary="returns list of member's contact requests.",
    description="This endpoint returns a list of the member's contact requests."
)
def requests(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...)):
    try:
        result = get_member_requests(db, member_id)
        if not result:
            raise HTTPException(status_code=404, detail="No contacts found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------list of searched contacts------------------------------------------------

@router.get("/search-contacts",response_model=List[MemberContacts],
    summary="returns list of contacts given a user id and search text.",
    description="This endpoint returns a list of contacts given a user id and search text."
)
def search_contacts(db: Session = Depends(get_db),
                    current_user: str = Depends(get_current_user), 
                    user_id:int = Query(...),
                    search_text:str = Query(...)
                    ):
    try:
        result = get_search_contacts(db, user_id, search_text)
        if not result:
            raise HTTPException(status_code=404, detail="No contacts found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-------------------------------------suggestions listing----------------------------------------------

@router.get("/suggestions",response_model=List[MemberContacts],
    summary="returns list of contacts suggested for a member .",
    description="This endpoint returns list of contacts suggested for a member."
)
def suggestions(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), member_id:int = Query(...)):
    try:
        result = get_member_suggestions(db, member_id)
        if not result:
            raise HTTPException(status_code=404, detail="No contacts found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))