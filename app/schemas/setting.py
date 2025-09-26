# app/schemas/setting.py

from typing import Optional
from pydantic import BaseModel

class NotificationsSetting (BaseModel):
    """Holds the system notifications to member info."""
    member_id : int
    send_msg : int
    add_as_friend : int
    confirm_friendship_request : int
    replies_to_your_help_quest : int
    
class PasswordData (BaseModel):
    """Holds the password info for member."""
    Pwd : bool 
    MemberID : bool

class MemberNameInfo(BaseModel): 
    """Holds member name info data."""
    first_name  : str
    last_name  : str
    middle_name  : str
    email  : str
    security_question  : str
    security_answer  : str
    password  : str
 
class PrivacySearchSettings(BaseModel):
    """Holds the privacy search settings data."""
    id: Optional[int] = None
    profile: Optional[int] = None
    basic_info: Optional[int] = None
    personal_info: Optional[int] = None
    photos_tag_of_you: Optional[int] = None
    videos_tag_of_you: Optional[int] = None
    contact_info: Optional[int] = None
    education: Optional[int] = None
    work_info: Optional[int] = None
    im_display_name: Optional[int] = None
    mobile_phone: Optional[int] = None
    other_phone: Optional[int] = None
    email_address: Optional[int] = None
    visibility: Optional[int] = None
    view_profile_picture: Optional[int] = None
    view_friends_list: Optional[int] = None
    view_Link_to_request_adding_you_as_friend: Optional[int] = None
    view_link_to_send_you_msg: Optional[int] = None
    email: Optional[str] = None


