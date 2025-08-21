# app/crud/member.py

from datetime import datetime
import os
import requests
from sqlalchemy.orm import aliased
from typing import List
from pytest import Session
from sqlalchemy import func, select, text

from app.db.models.sp_db_models import TbContacts, TbInterests, TbMemberFollowing, TbMemberPostResponses, TbMemberPosts, TbMemberProfileContactInfo, TbMemberProfileEducationV2, TbMemberProfiles, TbMembers
from app.schemas.member import ContactInfo, EducationInfo, GeneralInfo, PostResponses, Posts, YoutubeChannel, YoutubePlayList, YoutubeVideos, InstagramURL

#-----------------------------------------------------------------------------------

def get_recent_posts(member_id: int, db:Session) -> List[Posts]:
    # Step 1: Get list of contact IDs for the member
    contact_ids = (
        db.query(TbContacts.ContactID)
        .filter(TbContacts.MemberID == member_id)
        .all()
    )
    
    # Flatten result and include the original member
    contact_id_list = [cid[0] for cid in contact_ids]
    contact_id_list.append(member_id)

    # Step 2: Query posts by member and their contacts
    member_alias = aliased(TbMemberPosts)
    profile_alias = aliased(TbMemberProfiles)

    posts = (
        db.query(
            member_alias.PostID,
            member_alias.Title,
            member_alias.Description,
            member_alias.PostDate,
            member_alias.AttachFile,
            member_alias.MemberID,
            profile_alias.PicturePath,
            profile_alias.FirstName,
            profile_alias.LastName,
            member_alias.LikeCounter
        )
        .join(profile_alias, member_alias.MemberID == profile_alias.MemberID)
        .filter(member_alias.MemberID.in_(contact_id_list))
        .order_by(member_alias.PostDate.desc())
        .limit(50)
        .all()
    )

    # Step 3: Format into MemberPostsModel list
    result = []
    for post in posts:
        child_post_count = db.query(TbMemberPostResponses).filter(
            TbMemberPostResponses.PostID == post.PostID
        ).count()

        result.append(Posts(
            PostID=str(post.PostID),
            Title=post.Title or "",
            Description=post.Description or "",
            DatePosted=str(post.PostDate) if post.PostDate else "",
            AttachFile=post.AttachFile or "",
            MemberID=str(post.MemberID),
            PicturePath=post.PicturePath or "default.png",
            MemberName=f"{post.FirstName} {post.LastName}",
            FirstName=post.FirstName or "",
            ChildPostCnt=str(child_post_count),
            LikeCounter=post.LikeCounter
        ))

    return result

#-----------------------------------------------------------------------------------

def get_recent_post_responses(db: Session, post_id: int) -> List[PostResponses]:
    sql = text("EXEC spGetMemberChildPosts :PostID") 
    result = db.execute(sql, {"PostID": post_id})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [PostResponses(**row) for row in rows]

#-----------------------------------------------------------------------------------

def set_increment_post_like_counter(db: Session, post_id: int) -> None:
    sql = text("EXEC spIncrementLikeCounter :PostID")
    db.execute(sql, {"PostID": post_id})
    db.commit()

#-----------------------------------------------------------------------------------

def create_member_post(member_id: int, db: Session, post_msg: str) -> Posts | None:
    # Execute the stored procedure
    sql = text("EXEC spCreateMemberPost :MemberID, :PostMsg")
    db.execute(sql, {"MemberID": member_id, "PostMsg": post_msg})
    db.commit()

    # Table aliases
    post_alias = aliased(TbMemberPosts)
    profile_alias = aliased(TbMemberProfiles)

    # Correlated subquery for counting post responses
    child_post_count_subquery = (
        select(func.count(TbMemberPostResponses.PostID))
        .where(TbMemberPostResponses.PostID == post_alias.PostID)
        .correlate(post_alias)
        .scalar_subquery()
        .label("ChildPostCnt")
    )

    # Main query to fetch the most recent post
    result = (
        db.query(
            post_alias.PostID,
            post_alias.Title,
            post_alias.Description,
            post_alias.PostDate.label("DatePosted"),
            post_alias.AttachFile,
            post_alias.MemberID,
            profile_alias.PicturePath,
            profile_alias.FirstName,
            profile_alias.LastName,
            child_post_count_subquery,
            post_alias.LikeCounter
        )
        .join(profile_alias, post_alias.MemberID == profile_alias.MemberID)
        .filter(post_alias.MemberID == member_id)
        .order_by(post_alias.PostID.desc())
        .first()
    )

    if result:
        return Posts(
            PostID=str(result.PostID),
            Title=result.Title or "",
            Description=result.Description or "",
            DatePosted=str(result.DatePosted) if result.DatePosted else "",
            AttachFile=result.AttachFile or "",
            MemberID=str(result.MemberID),
            PicturePath=result.PicturePath or "default.png",
            MemberName=f"{result.FirstName} {result.LastName}",
            FirstName=result.FirstName or "",
            ChildPostCnt=str(result.ChildPostCnt),
            LikeCounter=result.LikeCounter
        )

    return None

#-----------------------------------------------------------------------------------

#def create_member_post_response(db: Session, member_id:int, post_id:int, post_msg:str) -> Posts | None:
def create_member_post_response(db: Session, member_id:int, post_id:int, post_msg:str) -> PostResponses | None:
    # Execute the stored procedure
    sql = text("EXEC spCreatePostComment :MemberID, :PostID, :PostMsg")
    db.execute(sql, {
        "MemberID": member_id,
        "PostID": post_id,
        "PostMsg": post_msg
    })
    db.commit()

    # Query to fetch the newly created comment
    response_alias = aliased(TbMemberPostResponses)
    profile_alias = aliased(TbMemberProfiles)

    result = (
        db.query(
            response_alias.PostResponseID,
            response_alias.Description,
            response_alias.ResponseDate,
            response_alias.MemberID,
            profile_alias.PicturePath,
            profile_alias.FirstName,
            profile_alias.LastName
        )
        .join(profile_alias, response_alias.MemberID == profile_alias.MemberID)
        .filter(response_alias.MemberID == member_id)
        .order_by(response_alias.PostResponseID.desc())
        .first()
    )

    if result:
        return PostResponses(
            PostID=post_id,
            PostResponseID=result.PostResponseID,
            Description=result.Description,
            DateResponded=str(result.ResponseDate),
            MemberID=result.MemberID,
            PicturePath=result.PicturePath,
            MemberName=f"{result.FirstName} {result.LastName}",
            FirstName=result.FirstName
        )

    return None

#-----------------------------------------------------------------------------------

def get_member_general_info(db: Session,member_id: int) -> GeneralInfo:
    # Left outer join setup using SQLAlchemy
    interest_alias = aliased(TbInterests)

    result = (
        db.query(
            TbMemberProfiles.MemberID,
            TbMemberProfiles.FirstName,
            TbMemberProfiles.MiddleName,
            TbMemberProfiles.LastName,
            TbMemberProfiles.Sex,
            TbMemberProfiles.ShowSexInProfile,
            TbMemberProfiles.DOBMonth,
            TbMemberProfiles.DOBDay,
            TbMemberProfiles.DOBYear,
            TbMemberProfiles.ShowDOBType,
            TbMemberProfiles.Hometown,
            TbMemberProfiles.HomeNeighborhood,
            TbMemberProfiles.CurrentStatus,
            TbMemberProfiles.InterestedInType,
            TbMemberProfiles.LookingForEmployment,
            TbMemberProfiles.LookingForRecruitment,
            TbMemberProfiles.LookingForPartnership,
            TbMemberProfiles.LookingForNetworking,
            TbMemberProfiles.Sport,
            TbMemberProfiles.Bio,
            TbMemberProfiles.Height,
            TbMemberProfiles.Weight,
            TbMemberProfiles.LeftRightHandFoot,
            TbMemberProfiles.PreferredPosition,
            TbMemberProfiles.SecondaryPosition,
            TbMemberProfiles.PicturePath,
            TbMemberProfiles.JoinedDate,
            TbMemberProfiles.CurrentCity,
            TbMemberProfiles.TitleDesc,
            interest_alias.InterestDesc
        )
        .outerjoin(
            interest_alias,
            TbMemberProfiles.InterestedInType == interest_alias.InterestID
        )
        .filter(TbMemberProfiles.MemberID == member_id)
        .first()
    )

    if not result:
        raise ValueError(f"No profile found for MemberID {member_id}")

    return GeneralInfo(
        MemberID=str(result.MemberID),
        FirstName=result.FirstName or "",
        MiddleName=result.MiddleName or "",
        LastName=result.LastName or "",
        Sex=result.Sex or "",
        ShowSexInProfile=result.ShowSexInProfile or False,
        DOBMonth=result.DOBMonth or "",
        DOBDay=result.DOBDay or "",
        DOBYear=result.DOBYear or "",
        ShowDOBType=result.ShowDOBType or False,
        Hometown=result.Hometown or "",
        HomeNeighborhood=result.HomeNeighborhood or "",
        CurrentStatus=str(result.CurrentStatus) if result.CurrentStatus is not None else "",
        InterestedInType=str(result.InterestedInType) if result.InterestedInType is not None else "",
        LookingForEmployment=result.LookingForEmployment or False,
        LookingForRecruitment=result.LookingForRecruitment or False,
        LookingForPartnership=result.LookingForPartnership or False,
        LookingForNetworking=result.LookingForNetworking or False,
        Sport=result.Sport or "",
        Bio=result.Bio or "",
        Height=result.Height or "",
        Weight=result.Weight or "",
        LeftRightHandFoot=result.LeftRightHandFoot or "",
        PreferredPosition=result.PreferredPosition or "",
        SecondaryPosition=result.SecondaryPosition or "",
        PicturePath=result.PicturePath or "",
        JoinedDate=str(result.JoinedDate) if result.JoinedDate else "",
        CurrentCity=result.CurrentCity or "",
        TitleDesc=result.TitleDesc or "",
        InterestedDesc=result.InterestDesc or ""
    )

#-----------------------------------------------------------------------------------

def get_member_contact_info(db: Session,member_id: int) -> ContactInfo:
    return (
        db.query(TbMemberProfileContactInfo)
        .filter(TbMemberProfileContactInfo.MemberID == member_id)
        .first()
    )

#-----------------------------------------------------------------------------------

#def get_member_education_info(db: Session, member_id: int) -> List[EducationInfo]:
def get_member_education_info(db: Session, member_id: int) -> List[EducationInfo]:
    education_list: List[EducationInfo] = []

    # Execute stored procedure
    result = db.execute(
        text("EXEC spGetMemberSchools :MemberID"),
        {"MemberID": member_id}
    )

    # Use .mappings() to get dictionary-like access to columns
    for row in result.mappings():
     education = EducationInfo(
        Degree=row.get("DegreeTypeDesc") or "",
        DegreeTypeID=str(row.get("DegreeType") or ""),  # Cast to str if needed
        SchoolAddress=row.get("Address") or "",
        SchoolID=int(row.get("SchoolID")) if row.get("SchoolID") is not None else None,
        SchoolImage=row.get("fileImage") or "",
        SchoolName=row.get("SchoolName") or "",
        YearClass=row.get("ClassYear") or "",
        SchoolType=str(row.get("SchoolType") or ""),  # Cast to str
        Major=row.get("Major") or "",
        SportLevelType=row.get("SportLevelType") or ""
        )
     education_list.append(education)

    return education_list

#-----------------------------------------------------------------------------------

def get_videos_list(playlist_id: str) -> List[YoutubeVideos]:
    # Load your API key from environment or configuration
    api_key = os.getenv("YOUTUBE_API_KEY", "")

    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "snippet",
        "playlistId": playlist_id,
        "maxResults": 50,
        "key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise exception on HTTP error

    items = response.json().get("items", [])
    videos = []

    for item in items:
        snippet = item.get("snippet", {})
        thumbnails = snippet.get("thumbnails", {})
        default_thumb = thumbnails.get("default", {})

        video = YoutubeVideos(
            Id=snippet.get("resourceId", {}).get("videoId", ""),
            Title=snippet.get("title", ""),
            Description=snippet.get("description", ""),
            Etag=item.get("etag", ""),
            PublishedAt=datetime.strptime(
                snippet.get("publishedAt", ""), "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%Y-%m-%d") if snippet.get("publishedAt") else "",
            DefaultThumbnail=default_thumb.get("url", ""),
            DefaultThumbnailHeight=str(default_thumb.get("height", "0")),
            DefaultThumbnailWidth=str(default_thumb.get("width", "0")),
        )
        videos.append(video)

    return videos

#-----------------------------------------------------------------------------------

def get_youtube_playlist(member_id: int, db:Session) -> List[YoutubePlayList]:
    playlists: List[YoutubePlayList] = []

    try:
        channel_id = get_youtube_channel(member_id, db)

        if channel_id:
            api_key = os.getenv("YOUTUBE_API_KEY", "")
            url = "https://www.googleapis.com/youtube/v3/playlists"
            params = {
                "part": "snippet",
                "channelId": channel_id,
                "maxResults": 50,
                "key": api_key
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            items = response.json().get("items", [])

            for item in items:
                snippet = item.get("snippet", {})
                thumbnails = snippet.get("thumbnails", {})
                default_thumb = thumbnails.get("default", {})

                playlist = YoutubePlayList(
                    Id=item.get("id", ""),
                    Title=snippet.get("title", ""),
                    Description=snippet.get("description", ""),
                    Etag=item.get("etag", ""),
                    DefaultThumbnail=default_thumb.get("url", ""),
                    DefaultThumbnailHeight=str(default_thumb.get("height", "") or "0"),
                    DefaultThumbnailWidth=str(default_thumb.get("width", "") or "0")
                )

                playlists.append(playlist)

    except Exception as e:
        # Optional: log the exception
        print(f"Error fetching playlist: {e}")

    return playlists


def get_youtube_channel(member_id: int, db: Session) -> str:
    member = (
        db.query(TbMembers)
        .filter(TbMembers.MemberID == member_id)
        .first()
    )

    if member:
        return member.YoutubeChannel or ""
    return ""

#-----------------------------------------------------------------------------------

def check_is_friend_by_contact_id(db: Session, member_id:int, contact_id:int) -> bool:
    exists = (
        db.query(TbContacts)
        .filter(
            TbContacts.MemberID == member_id,
            TbContacts.ContactID == contact_id
        )
        .first()
    )
    return exists is not None    

#-----------------------------------------------------------------------------------

def check_is_following_contact(db: Session, member_id:int, contact_id:int) -> bool:
    exists = (
        db.query(TbMemberFollowing)
        .filter(
            TbMemberFollowing.MemberId == member_id,
            TbMemberFollowing.FollowingMemberId == contact_id
        )
        .first()
    )
    return exists is not None    

#-----------------------------------------------------------------------------------

def save_member_general_info(db: Session, save_info: GeneralInfo ):
    sql = text("""
        EXEC spSaveMemberGeneralInfo 
            @MemberID=:MemberID, 
            @FirstName=:FirstName, 
            @MiddleName=:MiddleName, 
            @LastName=:LastName, 
            @Title=:Title, 
            @InterestIn=:InterestIn, 
            @CurrentStatus=:CurrentStatus, 
            @Gender=:Gender, 
            @ShowGender=:ShowGender, 
            @DOBMonth=:DOBMonth, 
            @DOBDay=:DOBDay, 
            @DOBYear=:DOBYear, 
            @ShowDOB=:ShowDOB, 
            @lookingForPartnership=:LookingForPartnership, 
            @lookingForEmployment=:LookingForEmployment, 
            @lookingForRecruitment=:LookingForRecruitment, 
            @lookingForNetworking=:LookingForNetworking, 
            @Sport=:Sport, 
            @Bio=:Bio, 
            @Height=:Height, 
            @Weight=:Weight, 
            @LeftRightHandFoot=:LeftRightHandFoot, 
            @PreferredPosition=:PreferredPosition, 
            @SecondaryPosition=:SecondaryPosition
    """)

    params = {
        "MemberID": save_info.MemberID,
        "FirstName": save_info.FirstName,
        "MiddleName": save_info.MiddleName,
        "LastName": save_info.LastName,
        "Title": save_info.TitleDesc,
        "InterestIn": save_info.InterestedInType,
        "CurrentStatus": save_info.CurrentStatus,
        "Gender": save_info.Sex,
        "ShowGender": save_info.ShowSexInProfile,
        "DOBMonth": save_info.DOBMonth,
        "DOBDay": save_info.DOBDay,
        "DOBYear": save_info.DOBYear,
        "ShowDOB": save_info.ShowDOBType,
        "LookingForPartnership": save_info.LookingForPartnership,
        "LookingForEmployment": save_info.LookingForEmployment,
        "LookingForRecruitment": save_info.LookingForRecruitment,
        "LookingForNetworking": save_info.LookingForNetworking,
        "Sport": save_info.Sport,
        "Bio": save_info.Bio,
        "Height": save_info.Height,
        "Weight": save_info.Weight,
        "LeftRightHandFoot": save_info.LeftRightHandFoot,
        "PreferredPosition": save_info.PreferredPosition,
        "SecondaryPosition": save_info.SecondaryPosition,
    }

    db.execute(sql, params)
    db.commit()

#-----------------------------------------------------------------------------------

def set_member_contact_info(db: Session, body:ContactInfo ):
    sql = text("""
        EXEC spSaveMemberContactInfo 
            @MemberID = :MemberID,
            @Email = :Email,
            @ShowEmailToMembers = :ShowEmailToMembers,
            @OtherEmail = :OtherEmail,
            @Facebook = :Facebook,
            @Instagram = :Instagram,
            @Twitter = :Twitter,
            @Website = :Website,
            @HomePhone = :HomePhone,
            @ShowHomePhone = :ShowHomePhone,
            @CellPhone = :CellPhone,
            @ShowCellPhone = :ShowCellPhone,
            @Address = :Address,
            @ShowAddress = :ShowAddress,
            @City = :City,
            @State = :State,
            @ZipCode = :ZipCode
    """)

    params = {
        "MemberID": body.MemberID,
        "Email": body.Email or "",
        "ShowEmailToMembers": body.ShowEmailToMembers,
        "OtherEmail": body.OtherEmail or "",
        "Facebook": body.Facebook or "",
        "Instagram": body.Instagram or "",
        "Twitter": body.Twitter or "",
        "Website": body.Website or "",
        "HomePhone": body.HomePhone or "",
        "ShowHomePhone": body.ShowHomePhone,
        "CellPhone": body.CellPhone or "",
        "ShowCellPhone": body.ShowCellPhone,
        "Address": body.Address or "",
        "ShowAddress": body.ShowAddress,
        "City": body.City or "",
        "State": body.State or "",
        "ZipCode": body.Zip or ""
    }

    db.execute(sql, params)
    db.commit()

#-----------------------------------------------------------------------------------

def get_instagram_url(db: Session, member_id: int) -> str:
    resp = (
        db.query(TbMemberProfileContactInfo)
        .filter(TbMemberProfileContactInfo.MemberID == member_id)
        .first()
    )

    return resp.Instagram if resp and resp.Instagram else ""

#-----------------------------------------------------------------------------------

def set_instagram_url(db: Session, data:InstagramURL) -> None:
    resp = (
        db.query(TbMemberProfileContactInfo)
        .filter(TbMemberProfileContactInfo.MemberID == data.MemberID)
        .first()
    )

    if resp:
        resp.Instagram = data.InstagramURL
        db.commit()

#-----------------------------------------------------------------------------------

def get_youtube_channel(db: Session, member_id: int) -> str:
    resp = (
        db.query(TbMembers)
        .filter(TbMembers.MemberID == member_id)
        .first()
    )

    return resp.YoutubeChannel if resp and resp.YoutubeChannel else ""

#-----------------------------------------------------------------------------------

def set_youtube_channel(db: Session, data:YoutubeChannel) -> None:
    resp = (
        db.query(TbMembers)
        .filter(TbMembers.MemberID == data.MemberID)
        .first()
    )

    if resp:
        resp.YoutubeChannel = data.ChannelID
        db.commit()

#-----------------------------------------------------------------------------------

def add_member_school(member_id:int, db: Session, data:EducationInfo) -> None:
    mp = TbMemberProfileEducationV2(
        MemberID=member_id,
        SchoolID=data.SchoolID,
        SchoolType=data.SchoolType,
        SchoolName=data.SchoolName,
        ClassYear=data.YearClass,
        Major=data.Major,
        DegreeType=data.DegreeTypeID,
        Societies="",
        SportLevelType=data.SportLevelType
    )
    db.add(mp)
    db.commit()

#-----------------------------------------------------------------------------------

def update_member_school(member_id:int, db: Session,data: EducationInfo) -> None:
    # Query the record
    mbr = (
        db.query(TbMemberProfileEducationV2)
        .filter(
            TbMemberProfileEducationV2.MemberID == member_id,
            TbMemberProfileEducationV2.SchoolID == data.SchoolID,
            TbMemberProfileEducationV2.SchoolType == data.SchoolType
        )
        .first()
    )
    # If found, update fields
    if mbr:
        mbr.ClassYear = data.YearClass
        mbr.Major = data.Major
        mbr.DegreeType = data.Degree
        mbr.Societies = ""
        mbr.SportLevelType = data.SportLevelType
        db.commit()

#-----------------------------------------------------------------------------------

def set_remove_school(db: Session, member_id: int, inst_id: int, inst_type: int) -> None:
    # Query the specific school record
    school_record = (
        db.query(TbMemberProfileEducationV2)
        .filter(
            TbMemberProfileEducationV2.MemberID == member_id,
            TbMemberProfileEducationV2.SchoolID == inst_id,
            TbMemberProfileEducationV2.SchoolType == inst_type
        )
        .first()
    )
    # If record exists, delete it
    if school_record:
        db.delete(school_record)
        db.commit()
