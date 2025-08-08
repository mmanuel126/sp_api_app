import datetime
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import text
from app.schemas.account import CodeAndNameForgotPwdModel, NewRegisteredUser, Register, User
from app.utils.crypto import encrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.models.sp_db_models import TbForgotPwdCodes, TbMembers, TbMemberProfiles, TbMembersRegistered
import logging
from app.utils.email import send_email
from app.utils.jwt import create_access_token, create_refresh_token
from app.core.config import settings 

def validate_user(db: Session, email: str, password: str) -> User | None:
    try:
        strPwd = encrypt(password)

        from sqlalchemy.orm import aliased

        Profile = aliased(TbMemberProfiles)

        query = (
            db.query(TbMembers, TbMemberProfiles)
            .join(Profile, TbMembers.MemberID == Profile.MemberID)
            .filter(
                TbMembers.Email == email,
                TbMembers.Password == strPwd,
                TbMembers.Status.in_([2, 3])
            )
            .first()
        )

        if query is None:
            return None

        m, p = query

        token_data = create_access_token({"sub": email})
        access_token = token_data["access_token"]
        expire_str = token_data["expire_date"]

        refresh_data = create_refresh_token({"sub": email})
        refresh_token = refresh_data["refresh_token"]
        refresh_expire_str = refresh_data["expire_date"]

        return User(
            memberID=str(m.MemberID),
            name=f"{p.FirstName} {p.LastName}",
            email=m.Email or "",
            picturePath=p.PicturePath or "",
            title=p.TitleDesc or "",
            currentStatus=str(m.Status or "0"),
            accessToken=access_token,
            expiredDate=expire_str,
            refreshToken=refresh_token,
            refreshExpireDate=refresh_expire_str
        )

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None


def validate_new_registered_user(db: Session, data:NewRegisteredUser) -> User | None:
    try:
        
        from sqlalchemy.orm import aliased

        Profile = aliased(TbMemberProfiles)

        query = (
            db.query(TbMembers, TbMemberProfiles,TbMembersRegistered)
            .join(Profile, TbMembers.MemberID == Profile.MemberID)
            .join(TbMembersRegistered, TbMembers.MemberID == TbMembersRegistered.MemberID)
            .filter(
                TbMembers.Email == data.email,
                TbMembersRegistered.MemberCodeID == data.code,
                TbMembers.Status.in_([1])
            )
            .first()
        )

        if query is None: return None

        m, p, _ = query #unpack all 3 models

        m.Status = 2 #update to active
        db.commit()

        token_data = create_access_token({"sub": data.email})
        access_token = token_data["access_token"]
        expire_str = token_data["expire_date"]

        refresh_data = create_refresh_token({"sub": data.email})
        refresh_token = refresh_data["refresh_token"]
        refresh_expire_str = refresh_data["expire_date"]

        return User(
            memberID=str(m.MemberID),
            name=f"{p.FirstName} {p.LastName}",
            email=m.Email or "",
            picturePath=p.PicturePath or "",
            title=p.TitleDesc or "",
            currentStatus=str(m.Status or "0"),
            accessToken=access_token,
            expiredDate=expire_str,
            refreshToken=refresh_token,
            refreshExpireDate=refresh_expire_str
        )

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None
 
   
def register_user(db: Session, user: Register) -> str | None:
    try:
        checkEmail = (
            db.query(TbMembers)
            .filter(
                TbMembers.Email == user.email
            )
            .first()
        )

        if checkEmail: return "ExistingEmail"

        strPwd = encrypt(user.password)
        code = create_new_user(db, user)

        if not code:
         raise HTTPException(status_code=500, detail="User creation failed")

        from_email = settings.APP_FROM_EMAIL
        to_email = user.email
        full_name = user.firstName + " " + user.lastName
        subject = "Account confirmation"
        body = generate_html_email_body(user.email,full_name, code, user.firstName,"web")
        send_email("", from_email, to_email, subject, body, True)

    except SQLAlchemyError as e:
        logging.error(f"Database error in validate_user: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error in validate_user: {e}")
        return None


def create_new_user(db: Session, user:Register) -> int:
   # raw connection for low-level DBAPI cursor
    conn = db.connection().connection
    cursor = conn.cursor()

    member_code = cursor.execute("""
        DECLARE @MemberCode INT;
        EXEC spCreateNewUser 
            @FirstName = ?, 
            @LastName = ?, 
            @Email = ?, 
            @Password = ?, 
            @Gender = ?, 
            @Month = ?, 
            @Day = ?, 
            @Year = ?, 
            @ProfileType = ?, 
            @MemberCode = @MemberCode OUTPUT;
        SELECT @MemberCode as MemberCode;
    """, user.firstname, user.lastname, user.email, user.password, user.gender, user.month, user.day, user.year, user.profileType)

    result = cursor.fetchone()
    return result.MemberCode if result else None


def generate_html_email_body(email: str, name: str, code: str, first_name: str, device: str) -> str:
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


def reset_password(db: Session, email:str) -> str:
    result_list = []

    # Join TbMembers and TbMemberProfiles
    profile = (
        db.query(TbMemberProfiles)
        .join(TbMembers, TbMemberProfiles.MemberID == TbMembers.MemberID)
        .filter(TbMembers.Email == email)
        .first()
    )

    if profile:
        # Insert new forgot pwd code
        new_code = TbForgotPwdCodes(
            Email=email,
            CodeDate=datetime.utcnow(),
            Status=0
        )
        db.add(new_code)
        db.commit()
        db.refresh(new_code)

        result_list.append(CodeAndNameForgotPwdModel(
            codeID=str(new_code.CodeID),
            firstName=profile.FirstName or ""
        ))
    else:
        # Email not found
        result_list.append(CodeAndNameForgotPwdModel(
            codeID="0",
            firstName=""
        ))

    if result_list:
        ds = result_list[0]
        code = ds.codeID
        first_name = ds.firstName

        from_email = settings.APP_FROM_EMAIL
        to_email = email
        #full_name = user.firstName + " " + user.lastName
        subject = "Password Reset confirmation"
        website_link = settings.WEBSITE_LINK
        app_name = settings.APP_NAME
        body = html_body_text(email,first_name, code, app_name,website_link)
        send_email(first_name, from_email, to_email, subject, body, True)
        return "success"
    else:
        return "fail"
    

def html_body_text(email: str, name: str, code: str, app_name: str, website_link: str) -> str:
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

def is_reset_code_expired(db: Session, code:str) -> str:
    flist = db.query(TbForgotPwdCodes).filter(
        TbForgotPwdCodes.CodeId == code,
        TbForgotPwdCodes.Status == 0
    ).all()
    if not flist:
        return "yes"
    else:
        return "no"
    

def change_password(db: Session, pwd:str, email:EmailStr, code: str) -> str:
    pwd_enc = encrypt(pwd)
    #if code is not empty then set it to expire
    if code:
        fedit = db.query(TbForgotPwdCodes).filter(
            TbForgotPwdCodes.CodeId == code
         ).first()
        fedit.Status = 1
        db.commit()  
    #change the password    
    sql = text("EXEC spChangePasswordViaEmail @Email=:email, @NewPwd=:pwd_enc")
    db.execute(sql, {"email": email, "new_pwd": pwd_enc})
    db.commit()   
    #return memberid:email if new email/pwd is validated
    user = validate_user(email,pwd)
    if user:
        return f"{user.memberID}:{user.email}"
    else:
        return ""






