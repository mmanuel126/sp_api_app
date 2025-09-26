#crud/contact.py 
# This module manages social interactions between members — think of it as the "friend system" behind the scenes. It supports:
    # * Searching for people
    # * Sending, accepting, and rejecting connection requests
    # * Following and unfollowing other users
    # * Getting lists of followers, followees, and contacts
    # * Receiving contact suggestions
    # * Sending messages as part of requests
    # * It uses stored procedures to handle most of the business logic on the database side.

from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session  
from typing import List
from app.db.models.sp_db_models import Tbcontactrequests, Tbmemberprofile, Tbmessages
from app.schemas.contact import MemberContacts, Search
from sqlalchemy import or_

#--------------------------------------------------------------------------------------

def get_search_results(db: Session, member_id: int, search_text: str) -> List[Search]:
    """
    Performs a general search for users or content using a stored procedure.
    Returns a list of search results (e.g., user profiles) matching the query.
    """

    sql = text("""
        SELECT * FROM public.sp_search_results(:memberid, :searchtext)
    """)
    result = db.execute(sql, {"memberid": member_id, "searchtext": search_text})
    rows = result.mappings().all()  # Get result rows as dict-like objects
    return [Search(**row) for row in rows]

#-----------------------------------------------------------------------------------

def get_people_iam_following(db: Session, member_id: int) -> List[MemberContacts]:
    """
    Returns a list of members the current user is following,
    using the `sp_get_followed_members` stored procedure.
    """

    sql = text("""
        SELECT * FROM public.sp_get_followed_members(:member_id)
    """)
    result = db.execute(sql, {"member_id": member_id})
    rows = result.fetchall()

    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]
  
#-----------------------------------------------------------------------------------

def get_whose_following_me(db: Session, member_id: int) -> List[MemberContacts]:
    """
    Returns a list of users who are following the current user.
    Maps `connection_id` from the DB to the `contact_id` field expected by the schema.
    """

    sql = text("""
        SELECT * FROM public.sp_get_whose_following_me(:member_id)
    """)
    result = db.execute(sql, {"member_id": member_id})
    rows = result.fetchall()
   
    contacts = []
    for row in rows:
        data = dict(row._mapping)

        # Map `connection_id` to `contact_id`
        if 'connection_id' in data:
            data['contact_id'] = data['connection_id']
        contacts.append(MemberContacts(**data))

    return contacts

#-----------------------------------------------------------------------------------

def set_follow_member(db: Session, member_id: int, contact_id: int) -> None:
    """
    Calls the stored procedure to follow another member.
    Adds the follow relationship in the DB.
    """

    sql = text("""
        SELECT public.sp_add_following_member(:member_id, :following_member_id)
    """)
    db.execute(sql, {"member_id": member_id, "following_member_id": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_unfollow_member(db: Session, member_id: int, contact_id: int) -> None:
    """
    Calls the stored procedure to unfollow a member.
    Removes the follow relationship.
    """
     
    sql = text("""
        SELECT public.sp_unfollow_member(:member_id, :following_member_id)
    """)
    db.execute(sql, {"member_id": member_id, "following_member_id": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_send_request(db: Session, member_id: int, contact_id: int, msg: str) -> None:
    """
    Sends a friend/contact request to another user.
    Also creates a message notifying the target member.
    """

    sql = text("""
        SELECT public.sp_send_friend_request(:member_id, :email)
    """)
    db.execute(sql, {"member_id": member_id, "email": str(contact_id)})
    db.commit()

    create_message(db, contact_id, member_id, "Requesting Contact", msg, "", "")

#-----------------------------------------------------------------------------------

def create_message(db: Session, to: int, from_: int, subject: str, body: str, attachment: str, original: str):
    """
    Creates and stores a message from one user to another.
    - Can be triggered by contact requests or direct messaging.
    - Saves the message to the `Tbmessages` table.
    """

    m = Tbmessages()
    m.sender_id = from_
    m.contact_id = to
    m.subject = subject
    m.msg_date = datetime.utcnow()
    m.body = body
    has_attachment = 0
    m.attachment = has_attachment
    m.message_state = 0
    m.attachment_file = attachment
    m.flag_level = 0
    m.importance_level = 0
    m.original_msg = original
    # Add and save
    db.add(m)
    db.commit()

#-----------------------------------------------------------------------------------

def get_member_contacts(db: Session, member_id: int) -> List[MemberContacts]:
    """
    Gets the current user's contacts (people they are connected with).
    Converts DB column `contact_member_id` to `contact_id`.
    Ensures `status` is a string (for frontend compatibility).
    """

    sql = text("""
        SELECT * FROM public.sp_get_member_contacts(:member_id, :show_type)
    """)
    result = db.execute(sql, {"member_id": member_id, "show_type": ""})
    rows = result.fetchall()

    contacts = []
    for row in rows:
        data = dict(row._mapping)

        # Map `member_contact_id` to `contact_id`
        if 'contact_member_id' in data:
            data['contact_id'] = data['contact_member_id']

        # Convert 'status' to string if it's not None
        if 'status' in data and data['status'] is not None:
            data['status'] = str(data['status'])

        contacts.append(MemberContacts(**data))

    return contacts


#-----------------------------------------------------------------------------------

def get_searched_member_contacts(db: Session, member_id: int, search_text:str) -> List[MemberContacts]:
    """
    Searches the user's contact list using a stored procedure.
    Returns matches as a list of `MemberContacts`.
    """

    sql = text("""
        SELECT * FROM public.sp_search_member_contacts(:member_id, :search_text)
    """)
    result = db.execute(sql, {"member_id": member_id, "search_text": search_text})
    rows = result.fetchall()
    # Convert row to dictionary and map to Pydantic schema
    return [MemberContacts(**row._mapping) for row in rows]

#-----------------------------------------------------------------------------------

def set_delete_contact(db: Session, member_id: int, contact_id: int) -> None:
    """
    Removes a contact relationship between the current user and another member.
    """

    sql = text("""
        SELECT public.sp_delete_contact(:member_id, :contact_id)
    """)
    db.execute(sql, {"member_id": member_id, "contact_id": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_accept_request(db: Session, member_id: int, contact_id: int) -> None:
    """
    Accepts a pending friend/contact request from another user.
    """

    sql = text("""
        SELECT public.sp_accept_request(:member_id, :contact_id)
    """)
    db.execute(sql, {"member_id": member_id, "contact_id": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def set_reject_request(db: Session, member_id: int, contact_id: int) -> None:
    """
    Rejects a pending contact/friend request.
    """

    sql = text("""
        SELECT public.sp_reject_request(:member_id, :contact_id)
    """)
    db.execute(sql, {"member_id": member_id, "contact_id": contact_id})
    db.commit()

#-----------------------------------------------------------------------------------

def get_member_requests(db: Session, member_id: int) -> list[MemberContacts]:
    """
    Retrieves a list of pending contact requests (people requesting to connect).
    Builds the result manually using joined data from `Tbmemberprofile` and `Tbcontactrequests`.
    """

    query = (
        db.query(
            Tbmemberprofile.first_name,
            Tbmemberprofile.last_name,
            Tbmemberprofile.picture_path,
            Tbmemberprofile.title_desc,
            Tbcontactrequests.from_member_id
        )
        .join(Tbcontactrequests, Tbmemberprofile.member_id == Tbcontactrequests.from_member_id)
        .filter(
            Tbcontactrequests.to_member_id == member_id,
            Tbcontactrequests.status == 0
        )
    )

    results = []
    for row in query.all():
        full_name = f"{row.first_name or ''} {row.last_name or ''}".strip()
        picture_path = row.picture_path if row.picture_path else "default.png"
        contact_id = str(row.from_member_id) if row.from_member_id is not None else ""

        results.append(MemberContacts(
            friend_name=full_name,
            first_name=row.first_name or "",
            picture_path=picture_path,
            contact_id=contact_id,
            title_desc=row.title_desc or "",
            show_type="",     # Optional default fields
            status="0",        # Optional default fields
            location = ""
        ))

    return results

#-----------------------------------------------------------------------------------

def get_search_contacts(db: Session, user_id: int, search_text: str) -> List[MemberContacts]:
    """
    Calls a stored procedure to search all users that match a search query,
    including those who are not yet contacts.
    Maps `connection_id` to `contact_id`.
    """

    sql = text("""
        SELECT  * FROM public.sp_get_search_contacts(:user_id, :search_text, :search_text2)
    """)

    params = {
        "user_id": user_id,
        "search_text": search_text,
        "search_text2": ""
    }
    result = db.execute(sql, params); 
    rows = result.fetchall()
   
    contacts = []
    for row in rows:
        data = dict(row._mapping)

        # Map `connection_id` to `contact_id`
        if 'connection_id' in data:
            data['contact_id'] = data['connection_id']
        contacts.append(MemberContacts(**data))

    return contacts

#-----------------------------------------------------------------------------------

def get_member_suggestions(db: Session, member_id: int) -> List[MemberContacts]:
    """
    Returns a list of suggested members to connect with.
    - Uses a raw DB cursor to call the `sp_get_member_suggestions` stored procedure.
    - Manually maps columns to the `MemberContacts` schema.
    - This might be used for "People You May Know" or onboarding suggestions.
    """
     
    connection = db.connection()
    raw_connection = connection.connection

    try:
        with raw_connection.cursor() as cursor:
            cursor.callproc("public.sp_get_member_suggestions", [member_id])
            columns = [col[0].lower() for col in cursor.description]
            rows = cursor.fetchall()

            suggestions = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                suggestion = MemberContacts(
                    contact_id=str(row_dict.get("contact_id", "")),
                    email=row_dict.get("email", ""),
                    first_name=row_dict.get("first_name", ""),
                    friend_name=row_dict.get("friend_name", ""),
                    label_text=row_dict.get("label_text", ""),
                    location=row_dict.get("location", ""),
                    name_and_id=row_dict.get("name_and_id", ""),
                    params=row_dict.get("params", ""),
                    paramsav=row_dict.get("paramsav", ""),
                    picture_path=row_dict.get("picture_path", ""),
                    show_type=row_dict.get("show_type", ""),
                    status=row_dict.get("status", ""),
                    title_desc=row_dict.get("title_desc", ""),
                    show_follow=row_dict.get("show_follow", "")
                )
                suggestions.append(suggestion)

            return suggestions

    finally:
        raw_connection.commit()  # Ensure changes (if any) are committed