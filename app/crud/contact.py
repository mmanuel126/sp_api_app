from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session  # Use this instead of pytest.Session
from typing import List
from app.db.models.sp_db_models import TbContactRequests, TbContacts, TbMemberProfileContactInfo, TbMemberProfiles, TbMessages, TbMessagesSent
from app.schemas.contact import MemberContacts, Search
from sqlalchemy import or_

def get_search_results(db: Session, member_id: int, search_text: str) -> List[Search]:
    sql = text("EXEC spSearchResults :MemberID, :SearchText")
    result = db.execute(sql, {"MemberID": member_id, "SearchText": search_text})
    # Use .mappings() to get rows as dictionaries
    rows = result.mappings().all()
    return [Search(**row) for row in rows]

#-----------------------------------------------------------------------------------

def get_people_iam_following(db: Session, member_id: int) -> List[MemberContacts]:
    sql = text("EXEC spGetFollowedMembers :MemberID")
    result = db.execute(sql, {"MemberID": member_id})
    rows = result.fetchall()

    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]
  
#-----------------------------------------------------------------------------------

def get_whose_following_me(db: Session, member_id: int) -> List[MemberContacts]:
    sql = text("EXEC spGetWhosFollowingMe :MemberID")
    result = db.execute(sql, {"MemberID": member_id})
    rows = result.fetchall()

    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]

#-----------------------------------------------------------------------------------

def set_follow_member(db: Session, member_id: int, contact_id: int) -> None:
    sql = text("EXEC spAddFollowingMember :MemberID, :FollowingMemberID")
    db.execute(sql, {"MemberID": member_id, "FollowingMemberID": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_unfollow_member(db: Session, member_id: int, contact_id: int) -> None:
    sql = text("EXEC spUnFollowMember :MemberID, :FollowingMemberID")
    db.execute(sql, {"MemberID": member_id, "FollowingMemberID": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_send_request(db: Session, member_id: int, contact_id: int, msg:str) -> None:
    sql = text("EXEC spSendFriendRequest :MemberID, :Email")
    db.execute(sql, {"MemberID": member_id, "Email": str(contact_id)})
    db.commit()
    create_message(db, contact_id,member_id, "Requesting Contact",msg, "","")

#-----------------------------------------------------------------------------------

def create_message(db: Session, to: int, from_: int, subject: str, body: str, attachment: str, original: str):
    # create new message objects
    m = TbMessages()
    ms = TbMessagesSent()

    m.SenderId = from_
    ms.SenderId = from_

    m.ContactId = to
    ms.ContactId = to

    m.Subject = subject
    ms.Subject = subject

    m.MsgDate = datetime.utcnow()
    ms.MsgDate = datetime.utcnow()

    m.Body = body
    ms.Body = body

    has_attachment = bool(attachment)
    m.Attachment = has_attachment
    ms.Attachment = has_attachment

    m.MessageState = 0
    ms.MessageState = 0

    m.AttachmentFile = attachment
    ms.AttachmentFile = attachment

    m.FlagLevel = 0
    ms.FlagLevel = 0

    m.ImportanceLevel = 0
    ms.ImportanceLevel = 0

    m.OriginalMsg = original
    ms.OriginalMsg = original

    # Add and save
    db.add(m)
    db.add(ms)
    db.commit()

#-----------------------------------------------------------------------------------

def get_member_contacts(db: Session, member_id: int) -> List[MemberContacts]:
    sql = text("EXEC spGetMemberContacts :MemberID, :ShowType")
    result = db.execute(sql, {"MemberID": member_id, "ShowType": ""})
    rows = result.fetchall()
    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]

#-----------------------------------------------------------------------------------

def get_searched_member_contacts(db: Session, member_id: int, search_text:str) -> List[MemberContacts]:
    sql = text("EXEC spSearchMemberContacts :MemberID, :searchText")
    result = db.execute(sql, {"MemberID": member_id, "searchText": search_text})
    rows = result.fetchall()
    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]

#-----------------------------------------------------------------------------------

def set_delete_contact(db: Session, member_id: int, contact_id: int) -> None:
    sql = text("EXEC spDeleteContact :MemberID, :ContactID")
    db.execute(sql, {"MemberID": member_id, "ContactID": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_accept_request(db: Session, member_id: int, contact_id: int) -> None:
    sql = text("EXEC spAcceptRequest :MemberID, :ContactID")
    db.execute(sql, {"MemberID": member_id, "ContactID": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_reject_request(db: Session, member_id: int, contact_id: int) -> None:
    sql = text("EXEC spRejectRequest :MemberID, :ContactID")
    db.execute(sql, {"MemberID": member_id, "ContactID": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def get_member_requests(db: Session, member_id: int) -> list[MemberContacts]:
    query = (
        db.query(
            TbMemberProfiles.FirstName,
            TbMemberProfiles.LastName,
            TbMemberProfiles.PicturePath,
            TbMemberProfiles.TitleDesc,
            TbContactRequests.FromMemberID
        )
        .join(TbContactRequests, TbMemberProfiles.MemberID == TbContactRequests.FromMemberID)
        .filter(
            TbContactRequests.ToMemberID == member_id,
            TbContactRequests.Status == 0
        )
    )

    results = []
    for row in query.all():
        full_name = f"{row.FirstName or ''} {row.LastName or ''}".strip()
        picture_path = row.PicturePath if row.PicturePath else "default.png"
        contact_id = str(row.FromMemberID) if row.FromMemberID is not None else ""

        results.append(MemberContacts(
            FriendName=full_name,
            FirstName=row.FirstName or "",
            PicturePath=picture_path,
            ContactID=contact_id,
            TitleDesc=row.TitleDesc or "",
            ShowType="",     # Optional default fields
            Status=0,        # Optional default fields
            Location = ""
        ))

    return results

#-----------------------------------------------------------------------------------

def get_search_contacts(db: Session, user_id: int, search_text: str) -> List[MemberContacts]:
    sql = text("""
        EXEC spGetSearchContacts :UserID, :SearchText, :SearchText2
    """)
    params = {
        "UserID": user_id,
        "SearchText": search_text,
        "SearchText2": ""
    }
    result = db.execute(sql, params).mappings().all()
    return [MemberContacts(**row) for row in result]

#-----------------------------------------------------------------------------------

def get_member_suggestions(db: Session, member_id: int) -> List[MemberContacts]:
    connection = db.connection()
    raw_connection = connection.connection

    try:
        with raw_connection.cursor() as cursor:
            cursor.callproc("spGetMemberSuggestions", [member_id])
            columns = [col[0].lower() for col in cursor.description]
            rows = cursor.fetchall()

            suggestions = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                suggestion = MemberContacts(
                    ContactID=str(row_dict.get("contactid", "")),
                    Email=row_dict.get("email", ""),
                    FirstName=row_dict.get("firstname", ""),
                    FriendName=row_dict.get("friendname", ""),
                    LabelText=row_dict.get("labeltext", ""),
                    Location=row_dict.get("location", ""),
                    NameAndID=row_dict.get("nameandid", ""),
                    Params=row_dict.get("params", ""),
                    ParamsAV=row_dict.get("paramsav", ""),
                    PicturePath=row_dict.get("picturepath", ""),
                    ShowType=row_dict.get("showtype", ""),
                    Status=row_dict.get("status", ""),
                    TitleDesc=row_dict.get("titledesc", ""),
                    ShowFollow=row_dict.get("showfollow", "")
                )
                suggestions.append(suggestion)

            return suggestions

    finally:
        raw_connection.commit()  # Ensure changes (if any) are committed