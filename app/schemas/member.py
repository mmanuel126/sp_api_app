# app/schemas/member.py

from typing import Optional
from pydantic import BaseModel

class Posts(BaseModel):
    post_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    date_posted: Optional[str] = None
    attach_file: Optional[str] = None
    member_id: Optional[int] = None
    picture_path: Optional[str] = None
    member_name: Optional[str] = None
    first_name: Optional[str] = None
    child_post_count: Optional[str] = None
    like_counter :Optional[int] = None

class PostResponses(BaseModel):
    post_response_id : Optional[int] = None
    post_id  :Optional[int] = None
    description: Optional[str] = None
    date_responded: Optional[str] = None
    member_id: Optional[int] = None
    member_name: Optional[str] = None
    first_name: Optional[str] = None
    picture_path: Optional[str] = None

class GeneralInfo (BaseModel):
    member_id: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    sex: Optional[str] = None
    show_sex_in_profile: Optional[bool] = None
    dob_month: Optional[str] = None
    dob_day: Optional[str] = None
    dob_year: Optional[str] = None
    show_dob_type: Optional[bool] = None
    home_town: Optional[str] = None
    home_neighborhood: Optional[str] = None
    current_status: Optional[str] = None
    interested_in_type: Optional[str] = None
    looking_for_employment: Optional[bool] = None
    looking_for_recruitment: Optional[bool] = None
    looking_for_partnership: Optional[bool] = None
    looking_for_networking: Optional[bool] = None
    picture_path: Optional[str] = None
    joined_date: Optional[str] = None
    current_city: Optional[str] = None
    title_desc: Optional[str] = None
    sport: Optional[str] = None
    bio: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    left_right_hand_foot: Optional[str] = None
    preferred_position: Optional[str] = None
    secondary_position: Optional[str] = None
    interested_desc: Optional[str] = None

class EducationInfo(BaseModel):
    degree: Optional[str] = ""
    degree_type_id: Optional[str] = ""   # Even if it's numeric in DB, treat as str if used that way
    school_address: Optional[str] = ""
    school_id: Optional[int] = None     # Accept None, not ""
    school_image: Optional[str] = ""
    school_name: Optional[str] = ""
    year_class: Optional[str] = ""
    school_type: Optional[str] = ""     # Cast to str in code
    major: Optional[str] = ""
    sport_level_type: Optional[str] = ""

    class Config:
        orm_mode = True

class YoutubeVideos(BaseModel): 
    etag  : Optional[str] = None
    id  : Optional[str] = None
    title : Optional[str] = None
    description : Optional[str] = None
    defaultThumbnail  : Optional[str] = None
    defaultThumbnailHeight  : Optional[str] = None
    defaultThumbnailWidth  : Optional[str] = None
    publishedAt  : Optional[str] = None

class YoutubePlayList(BaseModel):
    etag : Optional[str] = None
    id : Optional[str] = None
    title : Optional[str] = None
    description : Optional[str] = None
    defaultThumbnail : Optional[str] = None
    defaultThumbnailHeight : Optional[str] = None
    defaultThumbnailWidth : Optional[str] = None

class ContactInfo(BaseModel):
    member_id: Optional[int]= None
    email  : Optional[str] = None
    other_email  : Optional[str] = None
    facebook  : Optional[str] = None        
    instagram  : Optional[str] = None
    twitter  : Optional[str] = None
    website  : Optional[str] = None
    home_phone  : Optional[str] = None
    cell_phone  : Optional[str] = None
    other_phone : Optional[str] = None
    address  : Optional[str] = None
    city  : Optional[str] = None
    neighborhood  : Optional[str] = None
    state  : Optional[str] = None
    zip  : Optional[str] = None
    show_address  : Optional[bool] = None
    show_email_to_members  : Optional[bool] = None 
    show_cell_phone  : Optional[bool] = None
    show_home_phone  : Optional[bool] = None

    class Config:
        orm_mode = True

class InstagramURL(BaseModel):
     member_id : Optional[int] = None 
     instagram_url  : Optional[str] = None 


class YoutubeChannel(BaseModel):
    member_id : Optional[int] = None 
    channel_id  : Optional[str] = None 



