from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#convert to hashed password
def hash(password:str):
    return pwd_context.hash(password)

# verifying the plain_password and hashed_password
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)