# app/crud/setting.py
# This module handles all user settings-related database operations, including:
    # * Fetching and updating user profile info, privacy settings, notification preferences
    # * Changing email, password, and security question
    # * Deactivating accounts
    # * Interacting with both ORM models and a stored procedure for profile privacy

from typing import Optional
from pytest import Session
from sqlalchemy import text
from sqlalchemy.orm import aliased
from app.db.models.sp_db_models import Tbmemberprofile, Tbmembers, Tbmembersprivacysettings, Tbnotificationsettings
from app.schemas.setting import MemberNameInfo, NotificationsSetting, PrivacySearchSettings
from app.utils.crypto import encrypt

#-----------------------------------------------------------------------------------

def get_name_info(member_id: int, db: Session) -> Optional[MemberNameInfo]:
    # Retrieves personal and account-related info for a given user.

    # Create aliases to prevent naming conflict
    members = aliased(Tbmembers)
    profiles = aliased(Tbmemberprofile)

    result = (
        db.query(
            profiles.first_name,
            profiles.last_name,
            profiles.middle_name,
            members.email,
            members.security_question,
            members.security_answer,
            members.password
        )
        .join(profiles, members.member_id == profiles.member_id)
        .filter(members.member_id == member_id)
        .first()
    )

    if result:
        first, last, middle, email, security_q, security_a, password = result
        return MemberNameInfo(
            first_name=first or "",
            last_name=last or "",
            middle_name=middle or "",
            email=email or "",
            security_question=str(security_q) if security_q is not None else "",
            security_answer=security_a or "",
            password=password or ""
        )
    
    return None

#-----------------------------------------------------------------------------------

def get_notifications(member_id: int, db: Session) -> Optional[NotificationsSetting]:
    #Fetches the user's notification preferences.
    result = (
        db.query(
            Tbnotificationsettings.member_id,
            Tbnotificationsettings.send_msg,
            Tbnotificationsettings.add_as_friend,
            Tbnotificationsettings.confirm_friendship_request,
            Tbnotificationsettings.replies_to_your_help_quest
        )
        .filter(Tbnotificationsettings.member_id == member_id)
        .first()
    )

    if result:
        return NotificationsSetting(
            member_id=result.member_id,
            send_msg=result.send_msg or False,
            add_as_friend=result.add_as_friend or False,
            confirm_friendship_request=result.confirm_friendship_request or False,
            replies_to_your_help_quest=result.replies_to_your_help_quest or False
        )

    return None
    
#-----------------------------------------------------------------------------------------------

def set_update_name_info(db:Session, member_id:int, first_name:str, middle_name:str, last_name:str) -> None:
    # Updates the user's first, middle, and last name.
    mem = db.query(Tbmemberprofile).filter(Tbmemberprofile.member_id == member_id).first()
    if mem:
        mem.last_name = last_name
        mem.first_name = first_name
        mem.middle_name = middle_name
        db.commit()
    else:
        raise ValueError(f"Member with ID {member_id} not found.")

#-----------------------------------------------------------------------------------------------

def set_update_notifications(db:Session, member_id:int, body:NotificationsSetting) -> None:
    # Updates the user’s notification settings (e.g., messages, friend requests).
    ns = db.query(Tbnotificationsettings).filter(Tbnotificationsettings.member_id == member_id).first()
    if ns:
        ns.send_msg = body.send_msg
        ns.add_as_friend = body.add_as_friend
        ns.confirm_friendship_request = body.confirm_friendship_request
        ns.replies_to_your_help_quest = body.replies_to_your_help_quest
        db.commit()
    else:
        raise ValueError(f"Notification setting for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_update_email_info(db:Session, member_id:int, email:str) -> None:
    # Changes the user’s email address.
    exist = db.query(Tbmembers).filter(Tbmembers.email == email).first() 
    if exist: 
       raise ValueError(f"This email already exist on the system. Cannot have duplicate emails.") 
    else:   
        q = db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first()
        if q:
            q.email = email
            db.commit()
        else:
            raise ValueError(f"Email change for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_update_password_info(db:Session, member_id:int, password:str) -> None:
    # Updates and encrypts the user’s password.
    encryptPwd = encrypt(password)
    q = db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first()
    if q:
       q.password = encryptPwd
       db.commit()
    else:
        raise ValueError(f"Password change for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_security_question(db:Session, member_id:int, question_id:int, answer:str) -> None:
    # Updates the user's security question and answer.
    q = db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first()
    if q:
       q.security_question = question_id
       q.security_answer = answer
       db.commit()
    else:
        raise ValueError(f"Security Question Info for ID {member_id} not found.")  

#-----------------------------------------------------------------------------------------------

def set_deactivate_account(db:Session, member_id:int, reason:int, explanation:str, future_email:int) -> None:
    # Deactivates a user’s account.
    q = db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first()
    if q:
       q.status = 3
       q.deactivate_reason = reason
       q.deactivate_explanation = explanation
       q.future_emails = future_email
       db.commit()
    else:
        raise ValueError(f"Deactivate Account for ID {member_id} not found.")  

#-----------------------------------------------------------------------------------------------

def get_profile_settings(member_id: int, db: Session) -> PrivacySearchSettings:
    # Gets the user’s privacy and search visibility settings using stored procedure
    sql = text("""SELECT  * FROM public.sp_get_privacy_search_settings(:member_id) """)
    result = db.execute(sql, {"member_id": member_id})
    row = result.mappings().first()
    return PrivacySearchSettings(**row) 

#-----------------------------------------------------------------------------------------------

def set_profile_settings(member_id: int, db: Session,  body: PrivacySearchSettings) -> None:
    #Updates or inserts detailed profile privacy settings (e.g., what info is visible to others).
    p = db.query(Tbmembersprivacysettings).filter(Tbmembersprivacysettings.member_id == member_id).first()
    if p:
        p.member_id = member_id
        p.profile = body.profile
        p.basic_info = body.basic_info
        p.personal_info = body.personal_info
        p.photos_tag_of_you = body.photos_tag_of_you
        p.videos_tag_of_you = body.videos_tag_of_you
        p.contact_info = body.contact_info
        p.education = body.education
        p.work_info = body.work_info
        p.im_display_name = body.im_display_name
        p.mobile_phone = body.mobile_phone
        p.other_phone = body.other_phone
        p.email_address = body.email_address
    else:
        ps = Tbmembersprivacysettings(
            member_id=member_id,
            profile=body.profile,
            basic_info=body.basic_info,
            personal_info=body.personal_info,
            photos_tag_of_you=body.photos_tag_of_you,
            videos_tag_of_you=body.videos_tag_of_you,
            contact_info=body.contact_info,
            education=body.education,
            work_info=body.work_info,
            im_display_name=body.im_display_name,
            mobile_phone=body.mobile_phone,
            other_phone=body.other_phone,
            email_address=body.email_address
        )
        db.add(ps)
    db.commit()

#-----------------------------------------------------------------------------------------------

def privacy_search_settings(member_id: int, db: Session) -> PrivacySearchSettings:
    # Alias/helper to get profile settings using get_profile_settings.
    return get_profile_settings(member_id, db)

#-----------------------------------------------------------------------------------------------

def set_privacy_search_settings( member_id: int, db: Session,
    visibility: int,
    view_profile_picture: bool,
    view_friends_list:bool,
    view_link_to_Rquest_adding_you_as_friend:bool,
    view_link_to_send_you_msg:bool) -> None:
    #Updates high-level privacy settings like: who can see profile picture, friends list, and message or friend request link.
    p = db.query(Tbmembersprivacysettings).filter(Tbmembersprivacysettings.member_id == member_id).first()
    if p:
        p.member_id = member_id
        p.visibility = visibility
        p.view_profile_picture = view_profile_picture
        p.view_friends_list = view_friends_list
        p.view_link_to_request_adding_you_as_friend = view_link_to_Rquest_adding_you_as_friend
        p.view_link_to_send_you_msg = view_link_to_send_you_msg
    else:
        ps = Tbmembersprivacysettings(
            member_id = member_id,
            visibility = visibility,
            view_profile_picture = view_profile_picture,
            view_friends_list = view_friends_list,
            view_link_to_request_adding_you_as_friend = view_link_to_Rquest_adding_you_as_friend,
            view_link_to_send_you_msg = view_link_to_send_you_msg
        )
        db.add(ps)
    db.commit()