# app/schemas/member.py

from typing import Optional
from pydantic import BaseModel

class Posts(BaseModel):
    PostID: Optional[int] = None
    Title: Optional[str] = None
    Description: Optional[str] = None
    DatePosted: Optional[str] = None
    AttachFile: Optional[str] = None
    MemberID: Optional[int] = None
    PicturePath: Optional[str] = None
    MemberName: Optional[str] = None
    FirstName: Optional[str] = None
    ChildPostCnt: Optional[str] = None
    LikeCounter :Optional[int] = None

class PostResponses(BaseModel):
    PostResponseID : Optional[int] = None
    PostID  :Optional[int] = None
    Description: Optional[str] = None
    DateResponded: Optional[str] = None
    MemberID: Optional[int] = None
    MemberName: Optional[str] = None
    FirstName: Optional[str] = None
    PicturePath: Optional[str] = None

class GeneralInfo (BaseModel):
    MemberID: Optional[str] = None
    FirstName: Optional[str] = None
    MiddleName: Optional[str] = None
    LastName: Optional[str] = None
    Sex: Optional[str] = None
    ShowSexInProfile: Optional[bool] = None
    DOBMonth: Optional[str] = None
    DOBDay: Optional[str] = None
    DOBYear: Optional[str] = None
    ShowDOBType: Optional[bool] = None
    Hometown: Optional[str] = None
    HomeNeighborhood: Optional[str] = None
    CurrentStatus: Optional[str] = None
    InterestedInType: Optional[str] = None
    LookingForEmployment: Optional[bool] = None
    LookingForRecruitment: Optional[bool] = None
    LookingForPartnership: Optional[bool] = None
    LookingForNetworking: Optional[bool] = None
    PicturePath: Optional[str] = None
    JoinedDate: Optional[str] = None
    CurrentCity: Optional[str] = None
    TitleDesc: Optional[str] = None
    Sport: Optional[str] = None
    Bio: Optional[str] = None
    Height: Optional[str] = None
    Weight: Optional[str] = None
    LeftRightHandFoot: Optional[str] = None
    PreferredPosition: Optional[str] = None
    SecondaryPosition: Optional[str] = None
    InterestedDesc: Optional[str] = None

class EducationInfo(BaseModel):
    Degree: Optional[str] = ""
    DegreeTypeID: Optional[str] = ""   # Even if it's numeric in DB, treat as str if used that way
    SchoolAddress: Optional[str] = ""
    SchoolID: Optional[int] = None     # Accept None, not ""
    SchoolImage: Optional[str] = ""
    SchoolName: Optional[str] = ""
    YearClass: Optional[str] = ""
    SchoolType: Optional[str] = ""     # Cast to str in code
    Major: Optional[str] = ""
    SportLevelType: Optional[str] = ""

    class Config:
        orm_mode = True

class YoutubeVideos(BaseModel): 
    Etag  : Optional[str] = None
    Id  : Optional[str] = None
    Title : Optional[str] = None
    Description : Optional[str] = None
    DefaultThumbnail  : Optional[str] = None
    DefaultThumbnailHeight  : Optional[str] = None
    DefaultThumbnailWidth  : Optional[str] = None
    PublishedAt  : Optional[str] = None

class YoutubePlayList(BaseModel):
    Etag : Optional[str] = None
    Id : Optional[str] = None
    Title : Optional[str] = None
    Description : Optional[str] = None
    DefaultThumbnail : Optional[str] = None
    DefaultThumbnailHeight : Optional[str] = None
    DefaultThumbnailWidth : Optional[str] = None

class ContactInfo(BaseModel):
    MemberID: Optional[int]= None
    Email  : Optional[str] = None
    OtherEmail  : Optional[str] = None
    Facebook  : Optional[str] = None        
    Instagram  : Optional[str] = None
    Twitter  : Optional[str] = None
    Website  : Optional[str] = None
    HomePhone  : Optional[str] = None
    CellPhone  : Optional[str] = None
    Address  : Optional[str] = None
    City  : Optional[str] = None
    Neighborhood  : Optional[str] = None
    State  : Optional[str] = None
    Zip  : Optional[str] = None
    ShowAddress  : Optional[bool] = None
    ShowEmailToMembers  : Optional[bool] = None 
    ShowCellPhone  : Optional[bool] = None
    ShowHomePhone  : Optional[bool] = None

    class Config:
        orm_mode = True

class InstagramURL(BaseModel):
     MemberID : Optional[int] = None 
     InstagramURL  : Optional[str] = None 


class YoutubeChannel(BaseModel):
    MemberID : Optional[int] = None 
    ChannelID  : Optional[str] = None 



