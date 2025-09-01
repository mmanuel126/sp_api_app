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
    memberID: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    picturePath: Optional[str] = None
    title: Optional[str] = None
    currentStatus: Optional[str] = None
    accessToken: Optional[str] = None
    expiredDate: Optional[str] = None
    refreshToken: Optional[str] = None
    refreshExpireDate: Optional[str] = None
   

class Register (BaseModel):
    """Stores registered user info."""
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    day: str
    month: str
    year: str
    gender: str
    profileType: str    

class NewRegisteredUser (BaseModel):
    """Stores new registered user info."""
    email: EmailStr
    code: str

class CodeAndNameForgotPwdModel(BaseModel):
    """holds code and name forgot password data"""
    codeID: str
    firstName: str

