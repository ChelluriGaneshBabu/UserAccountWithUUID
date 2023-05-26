from fastapi import APIRouter,Depends,status,HTTPException,Header
from sqlalchemy.orm import Session
from app import schema,models,oauth2
from app.database import get_db

router = APIRouter(prefix= "/emails", tags= ["EMail"])

# @router.post("/",response_model= schema.VerifyToken, status_code= status.HTTP_201_CREATED)
# def email(email:schema.EmailIn, db:Session = Depends(get_db)):
#     # check if user_email already exist or not
#     email_data = db.query(models.Email).filter(models.Email.user_email == email.user_email).first()
#     if not email_data:
#         new_email = models.Email(**email.dict())
#         db.add(new_email)
#         db.commit()
#     data = db.query(models.Email).filter(models.Email.user_email == email.user_email).first()
#     # check the user_email registered or not
#     user_query = db.query(models.User).join(models.Email, models.Email.id == models.User.email_id, isouter=True).filter(models.Email.user_email == email.user_email).first()
#     if user_query:
#         raise HTTPException(status_code= status.HTTP_226_IM_USED, detail= "enter new email")
#     new_token = oauth2.generate_uuid()
#     # check if previously any token sent or not
#     user= db.query(models.Verify_Token).filter(models.Verify_Token.email_id == data.id).first()
#     if user:
#         user.token = new_token
#         db.commit()
#         return {"token":new_token}
#     else:
#         new_uuid = models.Verify_Token(email_id = data.id, token = new_token)
#         db.add(new_uuid)
#         db.commit()
#         return {"token":new_token}
    
@router.post("/",response_model= schema.VerifyToken, status_code= status.HTTP_201_CREATED)
def email(email:schema.EmailIn, db:Session = Depends(get_db)):
    # check if user_email already exist or not
    email_data = db.query(models.Email).filter(models.Email.user_email == email.user_email).first()
    if not email_data:
        new_email = models.Email(**email.dict())
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        # create token and save in data base
        new_token = oauth2.generate_uuid()
        new_uuid = models.Verify_Token(email_id = new_email.id, token = new_token)
        db.add(new_uuid)
        db.commit()
        return {"token":new_token}
    else:
    # check the user_email registered or not
        user_query = db.query(models.User).filter(models.User.email_id == email_data.id).first()
        if user_query:
            raise HTTPException(status_code= status.HTTP_226_IM_USED, detail= "enter new email")
        new_token = oauth2.generate_uuid()
        # get the previously stored token and override with new token
        user= db.query(models.Verify_Token).filter(models.Verify_Token.email_id == email_data.id).first()
        user.token = new_token
        db.commit()
        return {"token":new_token}