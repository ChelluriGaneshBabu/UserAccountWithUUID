from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app import schema,models,oauth2
from app.database import get_db


router = APIRouter(prefix= "/profile", tags= ["Profile"])

#create user profile
@router.post("/",response_model= schema.ProfileOut,status_code=status.HTTP_201_CREATED)
def create_user_profile(data:schema.Profile, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # check if profile data already exist or not
    profile_data = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if profile_data:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "user profile already exits")
    new_data = models.Profile(user_id = current_user.id, **data.dict())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    # to display both user and profile data in response
    profile_additional_data = db.query(models.User, models.Profile).join(models.Profile, models.User.id == models.Profile.user_id).filter(current_user.id == models.User.id).add_columns(models.User.first_name, models.User.last_name, models.User.phone_number, models.Profile.date_of_birth, models.Profile.address, models.Profile.highest_qualification, models.Profile.id).first()
    return profile_additional_data


# edit user profile
@router.put("/edit_profile")
def edit_profile(data:schema.EditProfile, db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    copy_data = data
    profile_data = db.query(models.Profile).filter(current_user.id == models.Profile.user_id).first()
    # check if profile data exist or not
    if not profile_data:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= "Profile not found")
    # updating in profile table
    for field, value in data.dict(exclude_unset = True).items():
        if value is not None:
            setattr(profile_data, field, value)
            
    user_data = db.query(models.User).filter(current_user.id == models.User.id).first()
    # updating in user table
    for field, value in copy_data.dict(exclude_unset = True).items():
        if value is not None:
            setattr(user_data, field, value)
    db.commit()
    # db.refresh(profile_data,user_data)
    return {"message":"updated successfully"}