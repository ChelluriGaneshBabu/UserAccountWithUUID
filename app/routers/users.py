from fastapi import APIRouter,Depends,status,HTTPException,Header,Response
from sqlalchemy.orm import Session
from app import schema,models,oauth2,utils
from app.database import get_db
from datetime import datetime


router = APIRouter(prefix= "/users",tags= ["Users"])
# verify email token and register
@router.post("/register",status_code= status.HTTP_201_CREATED, response_model= schema.UserOut)
def create_user(response:Response, user_data:schema.UserCreate, Authorization:str= Header(...),db:Session = Depends(get_db)):
    
    # check the token
    if Authorization == "None":
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "user already registerd")
    verified_user = db.query(models.Verify_Token).filter(models.Verify_Token.token == Authorization).first()
    if not verified_user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid token")
    
    # override the verified token with none value after register in postman environment variable
    response.headers.append("token","None")
    hashed_password = utils.hash(user_data.password)
    user_data.password = hashed_password
    new_user = models.User(email_id = verified_user.email_id, **user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#change to new password
@router.put("/change_password", status_code= status.HTTP_200_OK)
def change_password(password_data:schema.ChangePassword, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # verify the password
    if not utils.verify(password_data.old_password, current_user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Enter correct password")
    hashed_password = utils.hash(password_data.new_password)
    current_user.password = hashed_password
    current_user.modified_on = datetime.now()
    db.commit()
    return {"message":"password changed successfully"}

#forget password
@router.post("/forget_password", response_model= schema.VerifyToken, status_code= status.HTTP_201_CREATED)
def forget_password(email:schema.EmailIn, db:Session = Depends(get_db)):
    
    #check user is present in email table
    email_data = db.query(models.Email).filter(models.Email.user_email == email.user_email).first()
    if not email_data:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with {email.user_email} not found")
    
    # check user is registered or not
    verified_user = db.query(models.User).join(models.Email, models.Email.id == models.User.email_id, isouter=True).filter(models.Email.id == email_data.id).first()
    if not verified_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user {email.user_email} not registered found")
    access_token = oauth2.generate_uuid()
    new_token = models.Verify_Token(token = access_token, email_id = verified_user.email_id)
    db.add(new_token)
    db.commit()
    return {"token":access_token}

#set new password
@router.put("/set_new_password",status_code= status.HTTP_200_OK)
def set_new_password(password:schema.SetNewPassword, Authorization= Header(...), db:Session = Depends(get_db)):
    verified_user = db.query(models.User).join(models.Verify_Token, models.Verify_Token.email_id == models.User.email_id, isouter=True).filter(models.Verify_Token.token == Authorization).first()
    if not verified_user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid token")
    hashed_password = utils.hash(password.new_password)
    verified_user.password = hashed_password
    verified_user.modified_on = datetime.now()
    db.commit()
    return {"message":"password set successfully"}