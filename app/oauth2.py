import uuid
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from app.database import SessionLocal
from app import models
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from app import database



#  uuid token creation
def generate_uuid():
    new_uuid = str(uuid.uuid4())
    return new_uuid

oauth2_schema = OAuth2PasswordBearer(tokenUrl= "/login")

def verify_token(token:str,db:Session):
    token_data = db.query(models.AccessToken).filter(models.AccessToken.access_token == token).first()
    if token_data is None:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid token")
    return token_data

def get_current_user(access_token:str = Depends(oauth2_schema),db:Session=Depends(database.get_db)):
    token_data = verify_token(access_token,db)
    
    #check whether token expired or not
    if datetime.now() > token_data.expire_time:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "token has expired")
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if not user:
         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=  "user was not found")
    
    #extend the token expire time
    token_data.expire_time = token_data.expire_time + timedelta(minutes= 1)
    db.commit()
    return user
