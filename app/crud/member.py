# app/crud/member.py
# This module handles all data-related logic (CRUD operations) related to members of the application. It's responsible for:
# * Managing posts and comments
# * Tracking likes
# * Managing general profile info
# * Handling education history
# * Linking social media accounts (YouTube, Instagram)
# * Managing contacts and following/friend relationships
# * It uses SQLAlchemy for DB access and also uses some PostgreSQL stored procedures. It also connects with YouTube’s API to fetch videos and playlists from a member's channel.

from datetime import datetime
import os
from fastapi import Depends
import requests
from sqlalchemy.orm import aliased
from typing import List
from pytest import Session
from sqlalchemy import func, select, text
from app.db.models.sp_db_models import Tbcontacts, Tbinterests, Tbmemberfollowing, Tbmemberpostresponses, Tbmemberposts, Tbmemberprofile, Tbmemberprofilecontactinfo, Tbmemberprofileeducationv2, Tbmembers
from app.db.session import get_db
from app.schemas.member import ContactInfo, EducationInfo, GeneralInfo, PostResponses, Posts, YoutubeChannel, YoutubePlayList, YoutubeVideos, InstagramURL

#-----------------------------------------------------------------------------------

def get_recent_posts(member_id: int, db:Session) -> List[Posts]:
    # Step 1: Get list of contact IDs for the member
    contact_ids = (
        db.query(Tbcontacts.contact_id)
        .filter(Tbcontacts.member_id == member_id)
        .all()
    )
    
    # Flatten result and include the original member
    contact_id_list = [cid[0] for cid in contact_ids]
    contact_id_list.append(member_id)

    # Step 2: Query posts by member and their contacts
    member_alias = aliased(Tbmemberposts)
    profile_alias = aliased(Tbmemberprofile)

    posts = (
        db.query(
            member_alias.post_id,
            member_alias.title,
            member_alias.description,
            member_alias.post_date,
            member_alias.attach_file,
            member_alias.member_id,
            profile_alias.picture_path,
            profile_alias.first_name,
            profile_alias.last_name,
            member_alias.like_counter
        )
        .join(profile_alias, member_alias.member_id == profile_alias.member_id)
        .filter(member_alias.member_id.in_(contact_id_list))
        .order_by(member_alias.post_date.desc())
        .limit(50)
        .all()
    )

    # Step 3: Format into MemberPostsModel list
    result = []
    for post in posts:
        child_post_count = db.query(Tbmemberpostresponses).filter(
            Tbmemberpostresponses.post_id == post.post_id
        ).count()

        result.append(Posts(
            post_id=str(post.post_id),
            title=post.title or "",
            description=post.description or "",
            date_posted=str(post.post_date) if post.post_date else "",
            AttachFile=post.attach_file or "",
            member_id=str(post.member_id),
            picture_path=post.picture_path or "default.png",
            member_name=f"{post.first_name} {post.last_name}",
            first_name=post.first_name or "",
            child_post_count=str(child_post_count),
            like_counter=post.like_counter
        ))

    return result

#-----------------------------------------------------------------------------------

def get_recent_post_responses(db: Session, post_id: int) -> List[PostResponses]:
    sql = text(""" SELECT * FROM public.sp_get_member_child_posts( :post_id) """) 
    result = db.execute(sql, {"post_id": post_id})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [PostResponses(**row) for row in rows]

#-----------------------------------------------------------------------------------

def set_increment_post_like_counter(db: Session, post_id: int) -> None:
    sql = text(""" SELECT public.sp_increment_like_counter (:post_id) """)
    db.execute(sql, {"post_id": post_id})
    db.commit()

#-----------------------------------------------------------------------------------

def create_member_post(member_id: int, db: Session, post_msg: str) -> Posts | None:
    # Execute the stored procedure
    sql = text(""" SELECT public.sp_create_member_post(:member_id, :post_msg) """)
    db.execute(sql, {"member_id": member_id, "post_msg": post_msg})
    db.commit()

    # Table aliases
    post_alias = aliased(Tbmemberposts)
    profile_alias = aliased(Tbmemberprofile)

    # Correlated subquery for counting post responses
    child_post_count_subquery = (
        select(func.count(Tbmemberpostresponses.post_id))
        .where(Tbmemberpostresponses.post_id == post_alias.post_id)
        .correlate(post_alias)
        .scalar_subquery()
        .label("child_post_cnt")
    )

    # Main query to fetch the most recent post
    result = (
        db.query(
            post_alias.post_id,
            post_alias.title,
            post_alias.description,
            post_alias.post_date.label("date_posted"),
            post_alias.attach_file,
            post_alias.member_id,
            profile_alias.picture_path,
            profile_alias.first_name,
            profile_alias.last_name,
            child_post_count_subquery,
            post_alias.like_counter
        )
        .join(profile_alias, post_alias.member_id == profile_alias.member_id)
        .filter(post_alias.member_id == member_id)
        .order_by(post_alias.post_id.desc())
        .first()
    )

    if result:
        return Posts(
            post_id=str(result.post_id),
            title=result.title or "",
            description=result.description or "",
            date_posted=str(result.date_posted) if result.date_posted else "",
            attach_file=result.attach_file or "",
            member_id=str(result.member_id),
            picture_path=result.picture_path or "default.png",
            member_name=f"{result.first_name} {result.last_name}",
            first_name=result.first_name or "",
            child_post_cnt=str(result.child_post_cnt),
            like_counter=result.like_counter
        )

    return None

#-----------------------------------------------------------------------------------

def create_member_post_response(db: Session, member_id:int, post_id:int, post_msg:str) -> PostResponses | None:
    sql = text(""" SELECT public.sp_create_post_comment(:member_id, :post_id, :post_msg) """)
    db.execute(sql, {
        "member_id": member_id,
        "post_id": post_id,
        "post_msg": post_msg
    })
    db.commit()

    # Query to fetch the newly created comment
    response_alias = aliased(Tbmemberpostresponses)
    profile_alias = aliased(Tbmemberprofile)

    result = (
        db.query(
            response_alias.post_response_id,
            response_alias.description,
            response_alias.response_date,
            response_alias.member_id,
            profile_alias.picture_path,
            profile_alias.first_name,
            profile_alias.last_name
        )
        .join(profile_alias, response_alias.member_id == profile_alias.member_id)
        .filter(response_alias.member_id == member_id)
        .order_by(response_alias.post_response_id.desc())
        .first()
    )

    if result:
        return PostResponses(
            PostID=post_id,
            post_response_id=result.post_response_id,
            description=result.description,
            date_responded=str(result.response_date),
            member_id=result.member_id,
            picture_path=result.picture_path,
            member_name=f"{result.first_name} {result.last_name}",
            first_name=result.first_name
        )

    return None

#-----------------------------------------------------------------------------------

def get_member_general_info(db: Session,member_id: int) -> GeneralInfo:
    # Left outer join setup using SQLAlchemy
    interest_alias = aliased(Tbinterests)

    result = (
        db.query(
            Tbmemberprofile.member_id,
            Tbmemberprofile.first_name,
            Tbmemberprofile.middle_name,
            Tbmemberprofile.last_name,
            Tbmemberprofile.sex,
            Tbmemberprofile.show_sex_in_profile,
            Tbmemberprofile.dob_month,
            Tbmemberprofile.dob_day,
            Tbmemberprofile.dob_year,
            Tbmemberprofile.show_dob_type,
            Tbmemberprofile.hometown,
            Tbmemberprofile.home_neighborhood,
            Tbmemberprofile.current_status,
            Tbmemberprofile.interested_in_type,
            Tbmemberprofile.looking_for_employment,
            Tbmemberprofile.looking_for_recruitment,
            Tbmemberprofile.looking_for_partnership,
            Tbmemberprofile.looking_for_networking,
            Tbmemberprofile.sport,
            Tbmemberprofile.bio,
            Tbmemberprofile.height,
            Tbmemberprofile.weight,
            Tbmemberprofile.left_right_hand_foot,
            Tbmemberprofile.preferred_position,
            Tbmemberprofile.secondary_position,
            Tbmemberprofile.picture_path,
            Tbmemberprofile.joined_date,
            Tbmemberprofile.current_city,
            Tbmemberprofile.title_desc,
            interest_alias.interest_desc
        )
        .outerjoin(
            interest_alias,
            Tbmemberprofile.interested_in_type == interest_alias.interest_id
        )
        .filter(Tbmemberprofile.member_id == member_id)
        .first()
    )

    if not result:
        raise ValueError(f"No profile found for member_id {member_id}")

    return GeneralInfo(
        member_id=str(result.member_id),
        first_name=result.first_name or "",
        middle_name=result.middle_name or "",
        last_name=result.last_name or "",
        sex=result.sex or "",
        show_sex_in_profile=result.show_sex_in_profile or False,
        dob_month=result.dob_month or "",
        dob_day=result.dob_day or "",
        dob_year=result.dob_year or "",
        show_dob_type=result.show_dob_type or False,
        hometown=result.hometown or "",
        home_neighborhood=result.home_neighborhood or "",
        current_status=str(result.current_status) if result.current_status is not None else "",
        interested_in_type=str(result.interested_in_type) if result.interested_in_type is not None else "",
        looking_for_employment=result.looking_for_employment or False,
        looking_for_recruitment=result.looking_for_recruitment or False,
        looking_for_partnership=result.looking_for_partnership or False,
        looking_for_networking=result.looking_for_networking or False,
        sport=result.sport or "",
        bio=result.bio or "",
        height=result.height or "",
        weight=result.weight or "",
        left_right_hand_foot=result.left_right_hand_foot or "",
        preferred_position=result.preferred_position or "",
        secondary_position=result.secondary_position or "",
        picture_path=result.picture_path or "",
        joined_date=str(result.joined_date) if result.joined_date else "",
        current_city=result.current_city or "",
        title_desc=result.title_desc or "",
        interested_desc=result.interest_desc or ""
    )

#-----------------------------------------------------------------------------------

def get_member_contact_info(db: Session,member_id: int) -> ContactInfo:
    return (
        db.query(Tbmemberprofilecontactinfo)
        .filter(Tbmemberprofilecontactinfo.member_id == member_id)
        .first()
    )

#-----------------------------------------------------------------------------------

def get_member_education_info(db: Session, member_id: int) -> List[EducationInfo]:
    education_list: List[EducationInfo] = []

    sql =  text(""" 
            SELECT e.member_id, e.school_id, e.school_type, e.class_year, e.major, e.degree_type, 
                 e.societies, e.description,
                 d.degree_type_desc, e.sport_level_type, s.school_type_desc,

                (case e.school_type when 3  then
                    (select name from public.tbcolleges c where c.school_id=e.school_id) 
                    when 2 then
                        (select school_name  from public.tbprivateschools p  where p.lg_id = e.school_id)
                    when 1 then 
                        (select school_name  from public.tbpublicschools p  where p.lgid = e.school_id)
                    end ) as school_name,

                (case e.school_type when 3  then
                    (Select address From public.tbcolleges c  where c.school_id=e.school_id) 
                        when 2 then
                        (select school_name  from public.tbprivateschools p where p.lg_id = e.school_id)
                    when 1 then 
                        (select street_name || ', ' || city || ', ' || state || ' ' || zip
                         from public.tbpublicschools p where p.lgid = e.school_id)
                    end ) as address,

                (case e.school_type when 3  then
                    (Select c.website From public.tbcolleges c  where c.school_id=e.school_id) 
                    else
                        'default.png'
                    end ) as file_image
            
                    FROM public.tbmemberprofileeducationv2 e 
                    left JOIN public.tbdegreetype d on e.degree_type = d.degree_type_id
                    left JOIN public.tbschooltype s on e.school_type = s.school_type_id where member_id = :member_id 
                    Order by class_year desc
             """)
    
    result = db.execute(sql, {"member_id": member_id})

    # Use .mappings() to get dictionary-like access to columns
    for row in result.mappings():
     education = EducationInfo(
        degree=row.get("degree_type_desc") or "",
        degree_type_id=str(row.get("degree_type") or ""),  # Cast to str if needed
        school_address=row.get("address") or "",
        school_id=int(row.get("school_id")) if row.get("school_id") is not None else None,
        school_image=row.get("file_image") or "",
        school_name=row.get("school_name") or "",
        year_class=row.get("class_year") or "",
        school_type=str(row.get("school_type") or ""),  # Cast to str
        major=row.get("major") or "",
        sport_level_type=row.get("sport_level_type") or ""
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
            id=snippet.get("resourceId", {}).get("videoId", ""),
            title=snippet.get("title", ""),
            description=snippet.get("description", ""),
            etag=item.get("etag", ""),
            publishedAt=datetime.strptime(
                snippet.get("publishedAt", ""), "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%Y-%m-%d") if snippet.get("publishedAt") else "",
            defaultThumbnail=default_thumb.get("url", ""),
            defaultThumbnailHeight=str(default_thumb.get("height", "0")),
            defaultThumbnailWidth=str(default_thumb.get("width", "0")),
        )
        videos.append(video)

    return videos

#-----------------------------------------------------------------------------------

def get_youtube_playlist(member_id: int, db:Session) -> List[YoutubePlayList]:
    playlists: List[YoutubePlayList] = []

    try:
        member = (
        db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first())

        if member:
         channel_id = member.youtube_channel
        else:
            return "" 

        if channel_id:
            api_key = os.getenv("YOUTUBE_API_KEY", "")
            print(api_key)
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
                    id=item.get("id", ""),
                    title=snippet.get("title", ""),
                    description=snippet.get("description", ""),
                    etag=item.get("etag", ""),
                    defaultThumbnail=default_thumb.get("url", ""),
                    defaultThumbnailHeight=str(default_thumb.get("height", "") or "0"),
                    defaultThumbnailWidth=str(default_thumb.get("width", "") or "0")
                )

                playlists.append(playlist)
       
    except Exception as e:
        # Optional: log the exception
        print(f"Error fetching playlist: {e}")
    
    return playlists

#-----------------------------------------------------------------------------------

def check_is_friend_by_contact_id(db: Session, member_id:int, contact_id:int) -> bool:
    exists = (
        db.query(Tbcontacts)
        .filter(
            Tbcontacts.member_id == member_id,
            Tbcontacts.contact_id == contact_id
        )
        .first()
    )
    return exists is not None    

#-----------------------------------------------------------------------------------

def check_is_following_contact(db: Session, member_id:int, contact_id:int) -> bool:
    exists = (
        db.query(Tbmemberfollowing)
        .filter(
            Tbmemberfollowing.member_id == member_id,
            Tbmemberfollowing.following_member_id == contact_id
        )
        .first()
    )
    return exists is not None    

#-----------------------------------------------------------------------------------

def set_member_general_info(db: Session, data: GeneralInfo):
    profile = db.query(Tbmemberprofile).filter(Tbmemberprofile.member_id == data.member_id).first()

    if profile:
        # Update existing
        profile.first_name = data.first_name
        profile.middle_name = data.middle_name
        profile.last_name = data.last_name
        profile.title_desc = data.title_desc
        profile.interested_in_type = data.interested_in_type
        profile.current_status = data.current_status
        profile.sex = data.sex
        profile.show_sex_in_profile = data.show_sex_in_profile
        profile.dob_month = data.dob_month
        profile.dob_day = data.dob_day
        profile.dob_year = data.dob_year
        profile.show_dob_type = data.show_dob_type
        profile.looking_for_partnership = data.looking_for_partnership
        profile.looking_for_recruitment = data.looking_for_recruitment
        profile.looking_for_employment = data.looking_for_employment
        profile.looking_for_networking = data.looking_for_networking
        profile.sport = data.sport
        profile.bio = data.bio
        profile.height = data.height
        profile.weight = data.weight
        profile.left_right_hand_foot = data.left_right_hand_foot
        profile.preferred_position = data.preferred_position
        profile.secondary_position = data.secondary_position
    else:
        # Insert new
        profile = Tbmemberprofile(
            member_id = data.member_id,
            first_name = data.first_name,
            middle_name = data.middle_name,
            last_name = data.last_name,
            title_desc = data.title_desc,
            interested_in_type = data.interested_in_type,
            current_status = data.current_status,
            sex = data.sex,
            show_sex_in_profile = data.show_sex_in_profile,
            dob_month = data.dob_month,
            dob_day = data.dob_day,
            dob_year = data.dob_year,
            show_dob_type = data.show_dob_type,
            looking_for_partnership = data.looking_for_partnership,
            looking_for_recruitment = data.looking_for_recruitment,
            looking_for_employment = data.looking_for_employment,
            looking_for_networking = data.looking_for_networking,
            sport = data.sport,
            bio = data.bio,
            height = data.height,
            weight = data.weight,
            left_right_hand_foot = data.left_right_hand_foot,
            preferred_position = data.preferred_position,
            secondary_position = data.secondary_position
        )
        db.add(profile)

    db.commit()

#-----------------------------------------------------------------------------------

def set_member_contact_info(db: Session, data: Tbmemberprofilecontactinfo):
    # Try to fetch the existing record
    contact = db.get(Tbmemberprofilecontactinfo, data.member_id)

    if contact:
        # Update existing record
        contact.email = data.email
        contact.show_email_to_members = data.show_email_to_members
        contact.other_email = data.other_email
        contact.facebook = data.facebook
        contact.instagram = data.instagram
        contact.cell_phone = data.cell_phone
        contact.show_cell_phone = data.show_cell_phone
        contact.home_phone = data.home_phone
        contact.show_home_phone = data.show_home_phone
        contact.other_phone = data.other_phone
        contact.address = data.address
        contact.show_address = data.show_address
        contact.city = data.city
        contact.state = data.state
        contact.zip = data.zip
        contact.twitter = data.twitter
        contact.website = data.website
        contact.neighborhood = data.neighborhood
    else:
        # Insert new record
        contact = Tbmemberprofilecontactinfo(
            member_id=data.member_id,
            email=data.email,
            show_email_to_members=data.show_email_to_members,
            other_email=data.other_email,
            facebook=data.facebook,
            instagram=data.instagram,
            cell_phone=data.cell_phone,
            show_cell_phone=data.show_cell_phone,
            home_phone=data.home_phone,
            show_home_phone=data.show_home_phone,
            other_phone=data.other_phone,
            address=data.address,
            show_address=data.show_address,
            city=data.city,
            state=data.state,
            zip=data.zip,
            twitter=data.twitter,
            website=data.website,
            neighborhood=data.neighborhood
        )
        db.add(contact)

    db.commit()

#-----------------------------------------------------------------------------------

def get_instagram_url(db: Session, member_id: int) -> str:
    resp = (
        db.query(Tbmemberprofilecontactinfo)
        .filter(Tbmemberprofilecontactinfo.member_id == member_id)
        .first()
    )

    return resp.instagram if resp and resp.instagram else ""

#-----------------------------------------------------------------------------------

def set_instagram_url(db: Session, data:InstagramURL) -> None:
    resp = (
        db.query(Tbmemberprofilecontactinfo)
        .filter(Tbmemberprofilecontactinfo.member_id == data.member_id)
        .first()
    )

    if resp:
        resp.instagram = data.instagram_url
        db.commit()

#-----------------------------------------------------------------------------------

def get_youtube_channel(db: Session, member_id: int) -> str:
    resp = (
        db.query(Tbmembers)
        .filter(Tbmembers.member_id == member_id)
        .first()
    )

    return resp.youtube_channel if resp and resp.youtube_channel else ""

#-----------------------------------------------------------------------------------

def set_youtube_channel(db: Session, data:YoutubeChannel) -> None:
    resp = (
        db.query(Tbmembers)
        .filter(Tbmembers.member_id == data.member_id)
        .first()
    )

    if resp:
        resp.youtube_channel = data.channel_id
        db.commit()

#-----------------------------------------------------------------------------------

def add_member_school(member_id:int, db: Session, data:EducationInfo) -> None:
    mp = Tbmemberprofileeducationv2(
        member_id=member_id,
        school_id=data.school_id,
        school_type=data.school_type,
        school_name=data.school_name,
        class_year=data.year_class,
        major=data.major,
        degree_type=data.degree_type_id,
        societies="",
        sport_level_type=data.sport_level_type
    )
    db.add(mp)
    db.commit()

#-----------------------------------------------------------------------------------

def update_member_school(member_id:int, db: Session,data: EducationInfo) -> None:
    # Query the record
    mbr = (
        db.query(Tbmemberprofileeducationv2)
        .filter(
            Tbmemberprofileeducationv2.member_id == member_id,
            Tbmemberprofileeducationv2.school_id == data.school_id,
            Tbmemberprofileeducationv2.school_type == data.school_type
        )
        .first()
    )
    # If found, update fields
    if mbr:
        mbr.class_year = data.year_class
        mbr.major = data.major
        mbr.degree_type = data.degree_type_id
        mbr.societies = ""
        mbr.sport_level_type = data.sport_level_type
        db.commit()

#-----------------------------------------------------------------------------------

def set_remove_school(db: Session, member_id: int, inst_id: int, inst_type: int) -> None:
    # Query the specific school record
    school_record = (
        db.query(Tbmemberprofileeducationv2)
        .filter(
            Tbmemberprofileeducationv2.member_id == member_id,
            Tbmemberprofileeducationv2.school_id == inst_id,
            Tbmemberprofileeducationv2.school_type == inst_type
        )
        .first()
    )
    # If record exists, delete it
    if school_record:
        db.delete(school_record)
        db.commit()
