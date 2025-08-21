# app/schemas/setting.py

from typing import Optional
from pydantic import BaseModel

class NotificationsSetting (BaseModel):
    """Holds the system notifications to member info."""
    MemberID : int
    SendMsg : bool
    AddAsFriend : bool
    ConfirmFriendShipRequest : bool
    RepliesToYourHelpQuest : bool
    
class PasswordData (BaseModel):
    """Holds the password info for member."""
    Pwd : bool 
    MemberID : bool

class MemberNameInfo(BaseModel): 
    """Holds member name info data."""
    FirstName  : str
    LastName  : str
    MiddleName  : str
    Email  : str
    SecurityQuestion  : str
    SecurityAnswer  : str
    PassWord  : str
 
class PrivacySearchSettings(BaseModel):
    """Holds the privacy search settings data."""
    ID: Optional[int] = None
    Profile: Optional[int] = None
    BasicInfo: Optional[int] = None
    PersonalInfo: Optional[int] = None
    PhotosTagOfYou: Optional[int] = None
    VideosTagOfYou: Optional[int] = None
    ContactInfo: Optional[int] = None
    Education: Optional[int] = None
    WorkInfo: Optional[int] = None
    IMdisplayName: Optional[int] = None
    MobilePhone: Optional[int] = None
    OtherPhone: Optional[int] = None
    EmailAddress: Optional[int] = None
    Visibility: Optional[int] = None
    ViewProfilePicture: Optional[bool] = None
    ViewFriendsList: Optional[bool] = None
    ViewLinksToRequestAddingYouAsFriend: Optional[bool] = None
    ViewLinkTSendYouMsg: Optional[bool] = None
    Email: Optional[str] = None


