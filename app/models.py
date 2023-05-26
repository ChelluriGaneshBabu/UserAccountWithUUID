from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,BigInteger,Date,ForeignKey,DateTime
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer,primary_key=True)
    user_email = Column(String,unique=True ,nullable=False)

class Verify_Token(Base):
    __tablename__ = "verify_tokens"
    id = Column(Integer,primary_key=True)
    email_id = Column(Integer,ForeignKey("emails.id",ondelete="CASCADE"),nullable=False)
    token = Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email_id = Column(Integer,ForeignKey("emails.id",ondelete="CASCADE"),nullable=False)
    first_name = Column(String,nullable=False)
    last_name  = Column(String,nullable=False)
    phone_number=Column(BigInteger,nullable=False)
    password = Column(String,nullable=False)
    created_on=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    modified_on=Column(DateTime)
    
class AccessToken(Base):
    __tablename__ = "accesstokens"
    id = Column(Integer,primary_key=True)
    access_token = Column(String,nullable=False)
    expire_time = Column(TIMESTAMP,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    
class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer,primary_key=True)
    date_of_birth = Column(Date)
    address = Column(String)
    highest_qualification = Column(String)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
   