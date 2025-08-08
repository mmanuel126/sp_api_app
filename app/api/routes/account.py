# app/api/routes/account.py 

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from pytest import Session
from app.crud.account import change_password, is_reset_code_expired, reset_password, validate_user, validate_new_registered_user, register_user
from app.db.session import get_db
from app.schemas.account import Login, Register, NewRegisteredUser, User
from jose import JWTError, jwt
from app.core.config import settings
from app.utils.jwt import create_access_token


router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/login",response_model=User,
    summary="Log user in and create JWT token.",
    description="This endpoint authenticates a user and returns a JWT access token for use in secured endpoints."
)
def login(data: Login, db: Session = Depends(get_db)):
    # Authenticate user and create token
    user = validate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or credentials invalid")
    return user


@router.post("/loginNewRegisteredUser",response_model=User,
    summary="Login new registered user with a code.",
    description="This endpoint logs in a newly registered user with a code to account and stores their credentials securely."
)
def loginNewRegisteredUser(data: NewRegisteredUser, db: Session=Depends(get_db)):
    # logs in newly registered user
    user = validate_new_registered_user(db,data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or credentials invalid")
    return user


@router.get("/refreshLogin",
    summary="Refreshes a given token.",
    description="Given an access token this endpoint refreshes it as it is expired to allow login."
)
def refreshLogin(refresh_token: str = Query(..., description="JWT refresh token to refresh.")):
    try:
        # Decode token to get user identity
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create a new access token
        token_data = create_access_token({"sub": email})
        return {
            "accessToken": token_data["access_token"],
            "expiredDate": token_data["expire_date"]
        }

    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/register",
    summary="Register a new user.",
    description="This endpoint registers a new user account and stores their credentials securely."
)
def register(data: Register, db: Session = Depends(get_db)):
    # Register user
    response_str = register_user(db,data)
    if not response_str:
        raise HTTPException(status_code=404, detail="User not found or credentials invalid")
    return response_str


@router.get("/resetPassword",
    summary="Reset the passwored.",
    description="This endpoint resets the password given an email."
)
def resetPassword(email: str,db: Session = Depends(get_db)):
    # Reset password
    response_str = reset_password(db,email)
    if not response_str:
        raise HTTPException(status_code=500, detail="resseting password error.")
    return response_str  #success or fail


@router.get("/isResetCodeExpired",
    summary="Check if reset code expired.",
    description="This endpoint checks if reset code is expired. Returns the string 'yes' if it is and 'no' if not."
)
def isResetCodeExpired(code: str, db: Session = Depends(get_db)):
    # checks to see if code has expired
    response_str = is_reset_code_expired(db,code)
    if not response_str:
        raise HTTPException(status_code=500, detail="checking if code expired unexpected error.")
    return response_str  #yes or no


@router.get("/changePassword",
    summary="Changes the password.",
    description="this endpoint will take new password encrypt it and replaces the old one with it."
)
def changePassword(new_password: str,
     email: EmailStr ,
     code: str, db: Session = Depends(get_db)):
    # change password
    return change_password(db, new_password,email,code)