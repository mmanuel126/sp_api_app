# app/api/routes/member.py 

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pytest import Session

from app.auth.dependencies import get_current_user
from app.crud.member import add_member_school, check_is_following_contact, check_is_friend_by_contact_id, create_member_post, create_member_post_response, get_instagram_url, get_member_contact_info, get_member_education_info, get_member_general_info, get_recent_post_responses, get_recent_posts, get_videos_list, get_youtube_channel, get_youtube_playlist, set_increment_post_like_counter, set_instagram_url, set_member_contact_info, set_member_general_info, set_remove_school, set_youtube_channel, update_member_school
from app.db.models.sp_db_models import TbMemberProfileContactInfo
from app.db.session import get_db
from app.schemas.member import ContactInfo, EducationInfo, GeneralInfo, PostResponses, Posts, YoutubeChannel, YoutubePlayList, YoutubeVideos, InstagramURL

router = APIRouter(prefix="/member", tags=["Member"])

#-------------------------------  post related routes ----------------------------------------------------

@router.get("/posts/{member_id}",response_model=List[Posts],
    summary="Gets the list of recent posts.",
    description="This endpoint returns the list of member's recent posts listing."
)
def recent_posts(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        pst = get_recent_posts(member_id, db)
        if not pst:
            raise HTTPException(status_code=404, detail="Posts not found.")
        return pst
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/post-responses/{post_id}",response_model=List[PostResponses],
    summary="Gets the list of recent posts responses.",
    description="This endpoint returns the list of member's recent post responses listing."
)
def recent_post_respponses(post_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_recent_post_responses(db, post_id)
        if not resp:
            raise HTTPException(status_code=404, detail="Posts not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/increment-post-like-counter/{post_id}",
    summary="incremenet post like counter for post ID.",
    description="This endpoint increments post like counter for post ID."
)
def increment_post_like_counter(post_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        set_increment_post_like_counter(db, post_id)
        return {"message" : "incremented post like counter successfully."} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/create-post/{member_id}",
    summary="Creates post for member ID.",
    description="This endpoint creates a post for member ID."
)
def create_post(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user), post_msg:str=Query(...)):
    try:
        result = create_member_post(member_id, db,  post_msg)
        if not result:
            raise HTTPException(status_code=404, detail="Post not found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/create-post-response/{member_id}/{post_id}",
    summary="Creates post response for member ID.",
    description="This endpoint creates a post response for member ID and post ID"
)
def create_post_response(member_id:int, post_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user), post_msg:str=Query(...)):
    try:
        result = create_member_post_response(db, member_id, post_id, post_msg)
        if not result:
            raise HTTPException(status_code=404, detail="Post response not found.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#--------------------------------------member profile related routes ---------------------------------------------

@router.get("/general-info/{member_id}",response_model=GeneralInfo,
    summary="Gets the member profile general info.",
    description="This endpoint returns the member's profile general information."
)
def member_general_info(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_member_general_info(db, member_id)
        if not resp:
            raise HTTPException(status_code=404, detail="General info not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/contact-info/{member_id}",response_model=ContactInfo,
    summary="Gets the member contact info.",
    description="This endpoint returns the member's contact information."
)
def member_contact_info(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_member_contact_info(db, member_id)
        if not resp:
            raise HTTPException(status_code=404, detail="Contact info not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/education-info/{member_id}",response_model=List[EducationInfo],
    summary="Gets the member education info.",
    description="This endpoint returns the list of member's education information."
)
def member_education_info(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_member_education_info(db, member_id)
        if not resp:
            raise HTTPException(status_code=404, detail="Education info not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.get("/video-playlist/{member_id}",response_model=List[YoutubePlayList],
    summary="Gets u tube vidoe playlist",
    description="This endpoint returns the list of u tube video playlist."
)
def youtube_playlist(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_youtube_playlist(member_id, db)
        if not resp:
            raise HTTPException(status_code=404, detail="playlist not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
     
#-----------------------------------------------------------------------------------

@router.get("/youtube-videos/{playlist_id}",response_model=List[YoutubeVideos],
    summary="Gets the video list for a playerlist id.",
    description="This endpoint returns the list of youtube videos for a playerlist id."
)
def youtube_videos(playlist_id:str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_videos_list(playlist_id)
        if not resp:
            raise HTTPException(status_code=404, detail="youtuve playerlist not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/is-friend-by-contact-id/{member_id}/{contact_id}",response_model=bool,
    summary="checks if member is a contact by contact id.",
    description="This endpoint returns a bool to check to see if member is a contact by contact id."
)
def is_friend_by_contact_id(member_id, contact_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = check_is_friend_by_contact_id(db, member_id, contact_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#-----------------------------------------------------------------------------------

@router.get("/is-following-contact/{member_id}/{contact_id}",response_model=bool,
    summary="checks if member is following contact id.",
    description="This endpoint returns a bool to check to see if member is following contact id."
)
def is_following_contact(member_id, contact_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = check_is_following_contact(db, member_id, contact_id)
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    
#-----------------------------------------------------------------------------------

@router.post("/general-info",
    summary="Saves or update the member general info.",
    description="This endpoint saves or update the member general information."
)
def saves_member_general_info(
    data: GeneralInfo = Body(...), 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)):
     try:
         set_member_general_info(db, data)
         return {"message": "Saves general info successfully."}
     except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.post("/contact-info",
    summary="Saves or update the member contact info.",
    description="This endpoint saves or update the member contact information."
)
def saves_member_contact_info(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), data: ContactInfo = Body(...)):
    try:
        set_member_contact_info(db, data)
        return {"message": "Saves contact info successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#-----------------------------------------------------------------------------------

@router.get("/instagram-url/{member_id}",response_model=str,
    summary="Gets instagram url for the member id.",
    description="This endpoint returns the instagram url for the member id."
)
def instagram_url(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_instagram_url(db, member_id)
        if not resp:
            raise HTTPException(status_code=404, detail="Instagram url not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

#-----------------------------------------------------------------------------------

@router.put("/instagram-url",
    summary="Saves or update the member instagram url.",
    description="This endpoint saves or update the member instagram url."
)
def saves_instagram_url(data: InstagramURL = Body(...), db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        set_instagram_url(db, data)
        return {"message": "Saves instagram url successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    
    

@router.get("/youtube-channel/{member_id}",response_model=str,
    summary="Gets the youtube channel id for the member id.",
    description="This endpoint returns the youtube channel id for the member id."
)
def youtube_channel(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    try:
        resp = get_youtube_channel(db, member_id)
        if not resp:
            raise HTTPException(status_code=404, detail="Youtube channel id not found.")
        return resp
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

#-----------------------------------------------------------------------------------

@router.put("/youtube-channel",
    summary="Saves or update the member instagram url.",
    description="This endpoint saves or update the member instagram url."
)
def saves_youtube_channel(db: Session = Depends(get_db),current_user: str = Depends(get_current_user), data: YoutubeChannel = Body(...)):
    try:
        set_youtube_channel(db, data)
        return {"message": "Saves youtube channel successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
    
#-----------------------------------------------------------------------------------

@router.post("/add-school/{member_id}",
    summary="Add a school to list of schools for the member id.",
    description="This endpoint adds a school to list of schools for the member id."
)
def add_school(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user), data: EducationInfo = Body(...)):
    try:
        add_member_school(member_id, db, data)
        return {"message": "Added school successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
#-----------------------------------------------------------------------------------

@router.put("/update-school/{member_id}",
    summary="Update school info for the member id.",
    description="This endpoint updates school info for the member id."
)
def update_school(member_id:int, db: Session = Depends(get_db),current_user: str = Depends(get_current_user), data: EducationInfo = Body(...)):
    try:
        update_member_school(member_id, db, data)
        return {"message": "Updated school successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    
#-----------------------------------------------------------------------------------

@router.delete("/remove-school",
    summary="Removes a school for the member id.",
    description="This endpoint removes a school for the member id."
)
def remove_school(db: Session = Depends(get_db),current_user: str = Depends(get_current_user),  member_id: int = Query(...), inst_id: int = Query(...), inst_type: int = Query(...)):
    try:
        set_remove_school(db, member_id, inst_id, inst_type)
        return {"message": "Removed school successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   
    
    