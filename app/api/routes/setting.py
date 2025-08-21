# app/api/routes/setting.py

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pytest import Session

from app.auth.dependencies import get_current_user
from app.crud.setting import get_name_info, get_notifications, get_profile_settings, privacy_search_settings, set_deactivate_account, set_privacy_search_settings, set_profile_settings, set_security_question, set_update_email_info, set_update_name_info, set_update_notifications, set_update_password_info
from app.db.session import get_db
from app.schemas.setting import MemberNameInfo, NotificationsSetting, PrivacySearchSettings


router = APIRouter(prefix="/setting", tags=["Setting"])

#-----------------------------------------------------------------------------------

@router.get("/name-info/{member_id}",response_model=MemberNameInfo,
    summary="Get the member name info.",
    description="This endpoint returns the name of the member name information."
)
def name_info(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        name_info = get_name_info(member_id, db)
        if not name_info:
            raise HTTPException(status_code=404, detail="Name info not found.")
        return name_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/notifications/{member_id}",response_model=NotificationsSetting,
    summary="Get the member notifications.",
    description="This endpoint returns the member notifications."
)
def notifications(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        notifications = get_notifications(member_id, db)
        if not notifications:
            raise HTTPException(status_code=404, detail="Notifications not found.")
        return notifications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.put("/update-name-info/{member_id}",
    summary="Updates the member name info.",
    description="This endpoint updates the member name information."
)
def update_name_info(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  first_name: str = Query(...),
                  middle_name: str = Query(...),
                  last_name: str = Query(...),
                  ):
    try:
        set_update_name_info(db, member_id, first_name, middle_name, last_name)
        return {"message": "Updated member name successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.put("/update-notifications/{member_id}",
    summary="Updates the member notifications.",
    description="This endpoint updates the member notfications."
)
def update_notifications(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  body: NotificationsSetting = Body(...)
                  ):
    try:
        set_update_notifications(db, member_id, body)
        return {"message": "Updated notifications successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.put("/update-email-info/{member_id}",
    summary="Updates the member email.",
    description="This endpoint updates the member email."
)
def update_email_info(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  email: str = Query(...)
                  ):
    try:
        set_update_email_info(db, member_id, email)
        return {"message": "Updated member email successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.put("/save-password-info/{member_id}",
    summary="change the member's password.",
    description="This endpoint changes the member's password"
)
def save_password_info(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                  password: str = Query(...)
                  ):
    try:
        set_update_password_info(db, member_id, password)
        return {"message": "Updated member password successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.put("/save-security-question/{member_id}",
    summary="save the member's security questions.",
    description="This endpoint save the member's security questions."
)
def save_security_question(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                 question_id: int = Query(...),
                 answer: str = Query(...)
                  ):
    try:
        set_security_question(db, member_id, question_id, answer)
        return {"message": "Saved security question successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/deactivate-account/{member_id}",
    summary="Deactivate member account.",
    description="This endpoint deactivate member account."
)
def deactivate_account(member_id:int, db: Session = Depends(get_db),
                  current_user: str = Depends(get_current_user), 
                 reason: int = Query(...),
                 explanation: str = Query(...),
                 future_email: bool = Query(...)
                  ):
    try:
        set_deactivate_account(db, member_id, reason, explanation, future_email)
        return {"message": "Saved security question successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/profile-settings/{member_id}",response_model=PrivacySearchSettings,
    summary="Get the member profile settings.",
    description="This endpoint returns the members profile settings."
)
def profile_settings(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        psetting = get_profile_settings(member_id, db)
        if not psetting:
            raise HTTPException(status_code=404, detail="profile settings not found.")
        return psetting
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.put("/save-profile-settings/{member_id}",
    summary="Saves the member profile settings.",
    description="This endpoint saves the members profile settings."
)
def save_profile_settings(member_id:int,body: PrivacySearchSettings, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    try:
        set_profile_settings(member_id, db, body)
        return {"message": "Saved profile settings successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/privacy-search-settings/{member_id}",response_model=PrivacySearchSettings,
    summary="Get the member privacy search settings.",
    description="This endpoint returns the members privacy search settings."
)
def profile_search_settings(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        psetting = privacy_search_settings(member_id, db)
        if not psetting:
            raise HTTPException(status_code=404, detail="Privacy search settings not found.")
        return psetting
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.put("/save-privacy-search-settings/{member_id}",
    summary="Saves the privacy search settings.",
    description="This endpoint saves the members privacy search settings."
)
def profile_settings(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user),
            visibility:int = Query(...), view_profile_picture:bool= Query(...), 
        view_friends_list:bool = Query(...), view_link_to_Rquest_adding_you_as_friend:bool= Query(...),
            view_link_to_send_you_msg:bool = Query(...)):
    try:
        set_privacy_search_settings(member_id, db,
            visibility, view_profile_picture, 
            view_friends_list, view_link_to_Rquest_adding_you_as_friend,
            view_link_to_send_you_msg)
        return {"message": "Saved privacy search settings successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------
