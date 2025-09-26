# app/schemas/account.py

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    """Holds the log in data."""
    email: EmailStr
    password: str

class User(BaseModel):
    """ Holds the logged in user info."""
    member_id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    picture_path: Optional[str] = None
    title: Optional[str] = None
    current_status: Optional[str] = None
    access_token: Optional[str] = None
    expired_date: Optional[str] = None
    refresh_token: Optional[str] = None
    refresh_expire_date: Optional[str] = None
   

class Register (BaseModel):
    """Stores registered user info."""
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    day: str
    month: str
    year: str
    gender: str
    profile_type: str    

class NewRegisteredUser (BaseModel):
    """Stores new registered user info."""
    email: EmailStr
    code: str

class CodeAndNameForgotPwdModel(BaseModel):
    """holds code and name forgot password data"""
    code_id: str
    first_name: str

