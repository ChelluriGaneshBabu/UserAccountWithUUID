from typing import Optional
from pydantic import BaseModel,EmailStr,constr
from datetime import datetime,date
from typing import Optional
from app import models


class EmailIn(BaseModel):
    user_email:EmailStr

class VerifyToken(BaseModel):
    token:str
    class Config:
        orm_mode= True

class UserCreate(BaseModel):
    first_name :str
    last_name:str
    phone_number:constr(regex=r"^\+?[0-9]{10,12}$")
    password:str
    

class UserOut(BaseModel):
    id:int
    first_name :str
    last_name:str
    phone_number:constr(regex=r"^\+?[0-9]{10,12}$")
    created_on:datetime
    class Config:
        orm_mode= True

class Token(BaseModel):
    access_token:str

class ChangePassword(BaseModel):
    old_password:str
    new_password:str

class SetNewPassword(BaseModel):
    new_password:str

class Profile(BaseModel):
    date_of_birth:Optional[date]
    address:Optional[str]
    highest_qualification:Optional[str]

class ProfileOut(BaseModel):
    id:int
    first_name:str
    last_name:str
    phone_number:constr(regex=r"^\+?[0-9]{10,12}$")
    date_of_birth:date = None
    address:str = None
    highest_qualification:str = None
    class Config:
        orm_mode= True

class EditProfile(BaseModel):
      first_name:str=None
      last_name:str=None
      date_of_birth:date=None
      phone_number: constr(regex=r'^\+?[0-9]{10,12}$')=None
      address:str=None
      highest_qualification:str=None


    