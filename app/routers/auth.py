from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models,schema,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.conf import settings

router = APIRouter(tags= ["Authentication"])

#user login
@router.post("/login", status_code= status.HTTP_201_CREATED, response_model= schema.Token)
def user_login(login_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    # check user present or not
    user = db.query(models.User).join(models.Email, models.Email.id == models.User.email_id, isouter=True).filter(models.Email.user_email == login_data.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with {login_data.username} not found")
    if not utils.verify(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"INVALID CREDENTIALS")
    access_token = oauth2.generate_uuid()
    # create an expire time for token at the time of login
    token_expire_time = datetime.now() + timedelta(minutes= settings.access_token_expire_time)
    # save in data base
    new_token = models.AccessToken(access_token = access_token, expire_time = token_expire_time, user_id = user.id)
    db.add(new_token)
    db.commit()
    return {"access_token":access_token}