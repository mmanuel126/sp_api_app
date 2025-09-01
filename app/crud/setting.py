# app/crud/setting.py

from typing import Optional
from pytest import Session
from sqlalchemy import text
from sqlalchemy.orm import aliased

from app.db.models.sp_db_models import TbMemberProfiles, TbMembers, TbMembersPrivacySettings, TbNotificationSettings
from app.schemas.setting import MemberNameInfo, NotificationsSetting, PrivacySearchSettings
from app.utils.crypto import encrypt

#-----------------------------------------------------------------------------------

def get_name_info(member_id: int, db: Session) -> Optional[MemberNameInfo]:
    # Create aliases to prevent naming conflict
    members = aliased(TbMembers)
    profiles = aliased(TbMemberProfiles)

    result = (
        db.query(
            profiles.FirstName,
            profiles.LastName,
            profiles.MiddleName,
            members.Email,
            members.SecurityQuestion,
            members.SecurityAnswer,
            members.Password
        )
        .join(profiles, members.MemberID == profiles.MemberID)
        .filter(members.MemberID == member_id)
        .first()
    )

    if result:
        first, last, middle, email, security_q, security_a, password = result
        return MemberNameInfo(
            FirstName=first or "",
            LastName=last or "",
            MiddleName=middle or "",
            Email=email or "",
            SecurityQuestion=str(security_q) if security_q is not None else "",
            SecurityAnswer=security_a or "",
            PassWord=password or ""
        )
    
    return None

#-----------------------------------------------------------------------------------

def get_notifications(member_id: int, db: Session) -> Optional[NotificationsSetting]:
    result = (
        db.query(
            TbNotificationSettings.MemberID,
            TbNotificationSettings.LG_SendMsg,
            TbNotificationSettings.LG_AddAsFriend,
            TbNotificationSettings.LG_ConfirmFriendShipRequest,
            TbNotificationSettings.HE_RepliesToYourHelpQuest
        )
        .filter(TbNotificationSettings.MemberID == member_id)
        .first()
    )

    if result:
        return NotificationsSetting(
            MemberID=result.MemberID,
            SendMsg=result.LG_SendMsg or False,
            AddAsFriend=result.LG_AddAsFriend or False,
            ConfirmFriendShipRequest=result.LG_ConfirmFriendShipRequest or False,
            RepliesToYourHelpQuest=result.HE_RepliesToYourHelpQuest or False
        )

    return None
    
#eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjX21hbnVlbDJAaG90bWFpbC5jb20iLCJleHAiOjE3NTUzOTQ5NDl9.chmHh5GUX4YvC5Et_f2JP3FnI5LI_EjwTtVTRUrMaAI

#-----------------------------------------------------------------------------------------------

def set_update_name_info(db:Session, member_id:int, first_name:str, middle_name:str, last_name:str) -> None:
    mem = db.query(TbMemberProfiles).filter(TbMemberProfiles.MemberID == member_id).first()
    if mem:
        mem.LastName = last_name
        mem.FirstName = first_name
        mem.MiddleName = middle_name
        db.commit()
    else:
        raise ValueError(f"Member with ID {member_id} not found.")

#-----------------------------------------------------------------------------------------------

def set_update_notifications(db:Session, member_id:int, body:NotificationsSetting) -> None:
    ns = db.query(TbNotificationSettings).filter(TbNotificationSettings.MemberID == member_id).first()
    if ns:
        ns.LG_SendMsg = body.SendMsg
        ns.LG_AddAsFriend = body.AddAsFriend
        ns.LG_ConfirmFriendShipRequest = body.ConfirmFriendShipRequest
        ns.HE_RepliesToYourHelpQuest = body.RepliesToYourHelpQuest
        db.commit()
    else:
        raise ValueError(f"Notification setting for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_update_email_info(db:Session, member_id:int, email:str) -> None:
    q = db.query(TbMembers).filter(TbMembers.MemberID == member_id).first()
    if q:
       q.Email = email
       db.commit()
    else:
        raise ValueError(f"Email change for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_update_password_info(db:Session, member_id:int, password:str) -> None:
    encryptPwd = encrypt(password)
    q = db.query(TbMembers).filter(TbMembers.MemberID == member_id).first()
    if q:
       q.Password = encryptPwd
       db.commit()
    else:
        raise ValueError(f"Password change for ID {member_id} not found.")    

#-----------------------------------------------------------------------------------------------

def set_security_question(db:Session, member_id:int, question_id:int, answer:str) -> None:
    q = db.query(TbMembers).filter(TbMembers.MemberID == member_id).first()
    if q:
       q.SecurityQuestion = question_id
       q.SecurityAnswer = answer
       db.commit()
    else:
        raise ValueError(f"Security Question Info for ID {member_id} not found.")  

#-----------------------------------------------------------------------------------------------

def set_deactivate_account(db:Session, member_id:int, reason:int, explanation:str, future_email:bool) -> None:
    q = db.query(TbMembers).filter(TbMembers.MemberID == member_id).first()
    if q:
       q.Status = 3
       q.DeactivateReason = reason
       q.DeactivateExplanation = explanation
       q.FutureEmails = future_email
       db.commit()
    else:
        raise ValueError(f"Deactivate Account for ID {member_id} not found.")  

#-----------------------------------------------------------------------------------------------

def get_profile_settings(member_id: int, db: Session) -> PrivacySearchSettings:
    sql = text("EXEC spGetPrivacySearchSettings :MemberID") 
    result = db.execute(sql, {"MemberID": member_id})
    row = result.mappings().first()
    return PrivacySearchSettings(**row) 

#-----------------------------------------------------------------------------------------------

def set_profile_settings(member_id: int, db: Session,  body: PrivacySearchSettings) -> None:
    p = db.query(TbMembersPrivacySettings).filter(TbMembersPrivacySettings.MemberID == member_id).first()
    if p:
        p.MemberID = member_id
        p.Profile = body.Profile
        p.BasicInfo = body.BasicInfo
        p.PersonalInfo = body.PersonalInfo
        p.PhotosTagOfYou = body.PhotosTagOfYou
        p.VideosTagOfYou = body.VideosTagOfYou
        p.ContactInfo = body.ContactInfo
        p.Education = body.Education
        p.WorkInfo = body.WorkInfo
        p.ImdisplayName = body.IMdisplayName
        p.MobilePhone = body.MobilePhone
        p.OtherPhone = body.OtherPhone
        p.EmailAddress = body.EmailAddress
    else:
        ps = TbMembersPrivacySettings(
            MemberID=member_id,
            Profile=body.Profile,
            BasicInfo=body.BasicInfo,
            PersonalInfo=body.PersonalInfo,
            PhotosTagOfYou=body.PhotosTagOfYou,
            VideosTagOfYou=body.VideosTagOfYou,
            ContactInfo=body.ContactInfo,
            Education=body.Education,
            WorkInfo=body.WorkInfo,
            ImdisplayName=body.IMdisplayName,
            MobilePhone=body.MobilePhone,
            OtherPhone=body.OtherPhone,
            EmailAddress=body.EmailAddress
        )
        db.add(ps)
    db.commit()

#-----------------------------------------------------------------------------------------------

def privacy_search_settings(member_id: int, db: Session) -> PrivacySearchSettings:
    return get_profile_settings(member_id, db)

#-----------------------------------------------------------------------------------------------

def set_privacy_search_settings( member_id: int, db: Session,
    visibility: int,
    view_profile_picture: bool,
    view_friends_list:bool,
    view_link_to_Rquest_adding_you_as_friend:bool,
    view_link_to_send_you_msg:bool) -> None:
    p = db.query(TbMembersPrivacySettings).filter(TbMembersPrivacySettings.MemberID == member_id).first()
    if p:
        p.MemberID = member_id
        p.Visibility = visibility
        p.ViewProfilePicture = view_profile_picture
        p.ViewFriendsList = view_friends_list
        p.ViewLinkToRequestAddingYouAsFriend = view_link_to_Rquest_adding_you_as_friend
        p.ViewLinkToSendYouMsg = view_link_to_send_you_msg
    else:
        ps = TbMembersPrivacySettings(
            MemberID = member_id,
            Visibility = visibility,
            ViewProfilePicture = view_profile_picture,
            ViewFriendsList = view_friends_list,
            ViewLinkToRequestAddingYouAsFriend = view_link_to_Rquest_adding_you_as_friend,
            ViewLinkToSendYouMsg = view_link_to_send_you_msg
        )
        db.add(ps)
    db.commit()