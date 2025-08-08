# app/schemas/account.py

from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    """Holds the log in data."""
    email: EmailStr
    password: str

class User(BaseModel):
    """ Holds the logged in user info."""
    name: str
    title: str
    email: EmailStr
    memberID: str
    picturePath: str
    currentStatus: str
    accessToken: str
    expiredDate: str
    refreshToken: str
    refreshExpireDate: str

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
    codeID: str
    firstName: str