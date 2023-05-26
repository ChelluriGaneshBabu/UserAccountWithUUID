from app.conf import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.models import Base
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient
from app import schema

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush = False, autocommit = False, bind= engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# createing email and return token
@pytest.fixture
def created_email(client):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/emails/",json= email)
    assert res.status_code == 201
    token = schema.VerifyToken(**res.json())
    return token

# receiving token from created_email
@pytest.fixture
def authorized_client(client,created_email):
    client.headers["Authorization"]=created_email.token
    return client

# register in user account
@pytest.fixture
def registered_user(authorized_client):
    user_data = {"first_name":"ganesh","last_name":"chelluri","phone_number":9876543210,"password":"password"}
    res = authorized_client.post("/users/register",json= user_data)
    assert res.status_code == 201
    new_user = schema.UserOut(**res.json())
    return new_user

# createing email 2 and return token
@pytest.fixture
def created_email_2(client):
    email = {"user_email":"vamsi@gmail.com"}
    res = client.post("/emails/",json= email)
    assert res.status_code == 201
    token = schema.VerifyToken(**res.json())
    return token

# receiving token from created_email 2
@pytest.fixture
def authorized_client_2(client,created_email_2):
    client.headers["Authorization"]=created_email_2.token
    return client

# register in user account
@pytest.fixture
def registered_user_2(authorized_client_2):
    user_data = {"first_name":"vamsi","last_name":"chinni","phone_number":9012345678,"password":"password"}
    res = authorized_client_2.post("/users/register",json= user_data)
    assert res.status_code == 201
    new_user = schema.UserOut(**res.json())
    return new_user

# creating token for login user
@pytest.fixture
def login_user_token(client,registered_user_2):
    login_data = {"username":"vamsi@gmail.com","password":"password"}
    res= client.post("/login",data=login_data) # use data because the data is not in json format
    token = schema.Token(**res.json())
    assert res.status_code == 201
    return token

# receiving token from login user
@pytest.fixture
def authorized_user(client,login_user_token):
    client.headers["Authorization"]=f"Bearer {login_user_token.access_token}"
    return client


# creating token for registered user 2 forget password
@pytest.fixture
def registered_user_2_forget_password(client,registered_user_2):
    email = {"user_email":"vamsi@gmail.com"}
    res = client.post("/users/forget_password",json=email)
    assert res.status_code == 201
    token = schema.VerifyToken(**res.json())
    return token

# receiving token from registered user 2 forget password
@pytest.fixture
def authorized_user_who_forget_password(client,registered_user_2_forget_password):
    client.headers["Authorization"]= registered_user_2_forget_password.token
    return client

# creating user profile
@pytest.fixture
def create_user_2_profile(authorized_user):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"M-tech"}
    res = authorized_user.post("/profile/",json= data)
    assert res.status_code == 201
    new_data = res.json()
    return new_data