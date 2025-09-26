# app/crud/account.py -- This account.py module provides backend logic for managing user accounts in a FastAPI app, including:
    # * Logging in and validating users.
    # * Registering new users with email confirmation.
    # * Resetting and changing passwords securely.
    # * Generating and sending HTML-based emails.
    # * Creating and managing user status and codes via stored procedures and models.
    # * It handles both new registrations and existing user authentication, along with essential support for token generation, email communication, and password recovery workflows.

from datetime import datetime
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import text
from app.db.models.sp_db_models import Tbforgotpwdcodes, Tbmemberprofile, Tbmembers, Tbmembersregistered
from app.schemas.account import CodeAndNameForgotPwdModel, NewRegisteredUser, Register, User
from app.utils.crypto import encrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.utils.email import send_email
from app.utils.jwt import create_access_token, create_refresh_token
from app.core.config import settings 
from sqlalchemy.orm import aliased

def validate_user(db: Session, email: str, password: str) -> User | None:
    """
    Validates an existing user's credentials.
    - Encrypts the provided password.
    - Queries the database to match user with active status (2 or 3).
    - If match is found, returns user info with access and refresh tokens.
    - If not found, returns a blank user model with ID 0.
    """
    try:
        strPwd = encrypt(password)

        Profile = aliased(Tbmemberprofile)

        query = (
            db.query(Tbmembers, Tbmemberprofile)
            .join(Tbmemberprofile, Tbmembers.member_id == Tbmemberprofile.member_id)
            .filter(
                Tbmembers.email == email,
                Tbmembers.password == strPwd,
                Tbmembers.status.in_([2, 3])
            )
            .first()
        )

        if query is None:
            return User(
            member_id=str(0),
            name="",
            email=email or "",
            picture_path= "",
            title= "",
            current_status=str("0"),
            access_token="",
            expired_date="",
            refresh_token="",
            refresh_expire_date=""
            )

        m, p = query

        token_data = create_access_token({"sub": email})
        access_token = token_data["access_token"]
        expire_str = token_data["expire_date"]

        refresh_data = create_refresh_token({"sub": email})
        refresh_token = refresh_data["refresh_token"]
        refresh_expire_str = refresh_data["expire_date"]

        return User( 
            member_id=str(p.member_id),
            name=f"{p.first_name} {p.last_name}",
            email=p.email or "",
            picture_path=p.picture_path or "",
            title=p.title_desc or "",
            current_status=str(m.status or "0"),
            access_token=access_token,
            expired_date=expire_str,
            refresh_token=refresh_token,
            refresh_expire_date=refresh_expire_str
        )

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None

#-----------------------------------------------------------------------------------

def validate_new_registered_user(db: Session, data:NewRegisteredUser) -> User | None:
    """
    Validates a newly registered user by checking:
    - If the email and registration code match a pending (status 1) user.
    - If valid, updates status to active (2), generates access & refresh tokens.
    - Returns the full user model if successful, otherwise None.
    """
    try:
        Profile = aliased(Tbmemberprofile)
        query = (
            db.query(Tbmembers, Tbmemberprofile,Tbmembersregistered)
            .join(Profile, Tbmembers.member_id == Profile.member_id)
            .join(Tbmembersregistered, Tbmembers.member_id == Tbmembersregistered.member_id)
            .filter(
                Tbmembers.email == data.email,
                Tbmembersregistered.member_code_id == data.code,
                Tbmembers.status.in_([1])
            )
            .first()
        )

        if query is None: return None

        m, p, _ = query #unpack all 3 models

        m.status = 2 #update to active
        db.commit()

        token_data = create_access_token({"sub": data.email})
        access_token = token_data["access_token"]
        expire_str = token_data["expire_date"]

        refresh_data = create_refresh_token({"sub": data.email})
        refresh_token = refresh_data["refresh_token"]
        refresh_expire_str = refresh_data["expire_date"]

        return User(
            member_id=str(m.member_id),
            name=f"{p.first_name} {p.last_name}",
            email=m.email or "",
            picture_path=p.picture_path or "",
            title=p.title_desc or "",
            current_status=str(m.status or "0"),
            access_token=access_token,
            expired_date=expire_str,
            refresh_token=refresh_token,
            refresh_expire_date=refresh_expire_str
        )

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None
 
 #-----------------------------------------------------------------------------------
   
def register_user(db: Session, user: Register) -> str | None:
    """
    Registers a new user.
    - Checks if the email is already in use.
    - Encrypts the password.
    - Calls stored procedure to create the user (via create_new_user).
    - Sends a confirmation email with a registration code and link.
    - Returns "NewEmail" if successful, "ExistingEmail" if email exists.
    """
    try:
        checkEmail = (
            db.query(Tbmembers)
            .filter(
                Tbmembers.email == user.email
            )
            .first()
        )

        if checkEmail: return "ExistingEmail"

        strPwd = encrypt(user.password)
        user.password =strPwd
        code = create_new_user(db, user)

        if not code:
         raise HTTPException(status_code=500, detail="User creation failed")

        db.commit()
        from_email = settings.APP_FROM_EMAIL
        to_email = user.email
        full_name = user.first_name + " " + user.last_name
        subject = "Account confirmation"
        body = generate_html_email_body(user.email,full_name, code, user.first_name,"web")
        send_email("", from_email, to_email, subject, body, True)
        return "NewEmail"

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None

#-----------------------------------------------------------------------------------

def create_new_user(db: Session, user: Register) -> int:
    """
    Calls stored procedure `sp_create_new_user` to insert a new user into the database.
    - Passes basic user information as parameters.
    - Returns a registration code (MemberCode) if successful.
    """
    
    stmt = text("""
        SELECT sp_create_new_user(
            CAST(:FirstName AS VARCHAR),
            CAST(:LastName AS VARCHAR),
            CAST(:Email AS VARCHAR),
            CAST(:Password AS VARCHAR),
            CAST(:Gender AS VARCHAR),
            CAST(:Month AS VARCHAR),
            CAST(:Day AS VARCHAR),
            CAST(:Year AS VARCHAR),
            CAST(:ProfileType AS VARCHAR)
        ) AS MemberCode;
    """)

    result = db.execute(stmt, {
        "FirstName": user.first_name,
        "LastName": user.last_name,
        "Email": user.email,
        "Password": user.password,
        "Gender": user.gender,
        "Month": user.month,
        "Day": user.day,
        "Year": user.year,
        "ProfileType": user.profile_type,
     })
    row = result.fetchone()
    return row[0] if row else None

#-----------------------------------------------------------------------------------

def generate_html_email_body(email: str, name: str, code: str, first_name: str, device: str) -> str:
    """
    Generates HTML content for a registration confirmation email.
    - Includes a link to complete registration with the confirmation code.
    - Explains what the app is and what to expect after joining.
    """
    app_name = settings.APP_NAME
    website_link = settings.COMPLETE_REGISTRATION_LINK

    html_body = f"""
    <table width='100%' style='text-align: center;'>
        <tr>
            <td style='font-weight: bold; font-size: 12px; height: 25px; text-align: left; background-color: red;
                       vertical-align: middle; color: White;'>&nbsp;{app_name}
            </td>
        </tr>
        <tr><td>&nbsp;</td></tr>
        <tr>
            <td style='font-size: 12px; text-align: left; width: 100%; font-family: Trebuchet MS,Trebuchet,Verdana,Helvetica,Arial,sans-serif'>
                <p>Hi {name},</p>
            </td>
        </tr>
        <tr>
            <td style='font-size: 12px; text-align: left; width: 100%; font-family: Trebuchet MS,Trebuchet,Verdana,Helvetica,Arial,sans-serif'>
                <p>You recently registered for {app_name}. To complete your registration, click the link below
                (or copy/paste the link into a browser):</p>

                <p><a href='{website_link}?code={code}&email={email}&fname={first_name}&device={device}'>
                {website_link}?code={code}&email={email}&device={device}</a></p>

                <p>Your registration code is: {code}</p>

                <p>{app_name} is an exciting new sport social networking site that helps athletes showcase their talents 
                so they can potentially attract sport agents. It is also a tool for people to communicate and stay 
                connected with other sport fanatics. Once you become a member, you'll be able to share your sport 
                experience with the rest of the world.</p>

                <p>Thanks.<br />
                {app_name} Team<br /></p>
            </td>
        </tr>
    </table>
    """
    return html_body.strip()

#-----------------------------------------------------------------------------------

def reset_password(db: Session, email: str) -> str:
    """
    Handles password reset process.
    - Checks if a user with the given email exists.
    - If yes, creates a new reset code and saves it in the DB.
    - Sends an email with the reset code and instructions.
    - Returns 'success' if email sent, otherwise 'fail'.
    """
    result_list = []
    # Avoid duplicate joins by using the relationship
    MemberAlias = aliased(Tbmembers)

    profile = (
    db.query(Tbmemberprofile)
    .join(MemberAlias, Tbmemberprofile.member_id == MemberAlias.member_id)
    .filter(MemberAlias.email == email)
    .first()
)

    if profile:
        new_code = Tbforgotpwdcodes(
            email=email,
            codedate=datetime.utcnow(),
            status=0
        )
        db.add(new_code)
        db.commit()
        db.refresh(new_code)

        result_list.append(CodeAndNameForgotPwdModel(
            code_id=str(new_code.code_id),
            first_name=profile.first_name or ""
        ))
    else:
        result_list.append(CodeAndNameForgotPwdModel(
            code_id="0",
            first_name=""
        ))

    if result_list:
        ds = result_list[0]
        code = ds.code_id
        first_name = ds.first_name

        from_email = settings.APP_FROM_EMAIL
        to_email = email
        subject = "Password Reset confirmation"
        website_link = settings.WEBSITE_LINK
        app_name = settings.APP_NAME
        body = html_body_text(email, first_name, code, app_name, website_link)

        send_email(first_name, from_email, to_email, subject, body, True)
        return "success"
    else:
        return "fail"
    
#-----------------------------------------------------------------------------------

def html_body_text(email: str, name: str, code: str, app_name: str, website_link: str) -> str:
    """
    Generates the HTML body for a password reset email.
    - Includes a one-time reset code.
    - Warns users not to share it.
    """
    return f"""
    <table width='100%' style='text-align: center;'>
        <tr>
            <td style='font-weight: bold; font-size: 12px; height: 25px; text-align: left; background-color: #4a6792;
                vertical-align: middle; color: White;'>&nbsp;{app_name}</td>
        </tr>
        <tr><td>&nbsp;</td></tr>
        <tr>
            <td style='font-size: 12px; text-align: left; width: 100%; 
                font-family: Trebuchet MS, Trebuchet, Verdana, Helvetica, Arial, sans-serif'>
                <p>Hi {name},</p>
            </td>
        </tr>
        <tr>
            <td style='font-size: 12px; text-align: left; width: 100%; 
                font-family: Trebuchet MS, Trebuchet, Verdana, Helvetica, Arial, sans-serif'>
                <p>You recently requested a new password.</p>
                <p>Here is your reset code, which you can enter on the password reset page:<br/><b>{code}</b></p>
                <p>Do not share this code. We will never call or text you for it.</p>
                <p>If you did not request to reset your password, please disregard this message.</p>
                <p>Thanks.<br/>
                The {app_name} staff</p>
            </td>
        </tr>
    </table>
    """

#-----------------------------------------------------------------------------------

def is_reset_code_expired(db: Session, code:str) -> str:
    """
    Checks if a password reset code is expired.
    - Returns 'yes' if the code doesn't exist or is marked as used.
    - Returns 'no' if the code is still valid (status = 0).
    """
    flist = db.query(Tbforgotpwdcodes).filter(
        Tbforgotpwdcodes.code_id == code,
        Tbforgotpwdcodes.status == 0
    ).all()
    if not flist:
        return "yes"
    else:
        return "no"
    
#-----------------------------------------------------------------------------------

def change_password(db: Session, pwd:str, email:EmailStr, code: str) -> str:
    """
    Changes a user's password.
    - Encrypts the new password.
    - Marks the reset code as used (if provided).
    - Calls stored procedure to change the password in DB.
    - Validates the new credentials and returns 'member_id:email' if successful.
    - Returns empty string if validation fails.
    """
    pwd_enc = encrypt(pwd)
    #if code is not empty then set it to expire
    if code:
        fedit = db.query(Tbforgotpwdcodes).filter(
            Tbforgotpwdcodes.code_id == code
         ).first()
        if fedit:
            fedit.Status = 1
            db.commit()
        else:
            return {"message": "Invalid or expired reset code {code}."}
        
    #change the password    
    sql = text("SELECT sp_change_password_via_email(:email, :new_pwd)")
    db.execute(sql, {"email": email, "new_pwd": pwd_enc})
    db.commit()   
    #return memberid:email if new email/pwd is validated
    user = validate_user(db, email,pwd)
    if user:
        return f"{user.member_id}:{user.email}"
    else:
        return ""
    
#-----------------------------------------------------------------------------------

def set_member_status(db: Session, member_id: int, status: int) -> None:
    """
    Updates a member's status (e.g., activate, deactivate, etc.).
    - Commits the change if the user is found.
    """
    member = db.query(Tbmembers).filter(Tbmembers.member_id == member_id).first()
    if member:
        member.status = status
        db.commit()    






