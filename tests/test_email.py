from app import schema


# creating email
def test_creating_email(client):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/emails/",json= email)
    token = schema.VerifyToken(**res.json())
    assert res.status_code == 201

# send token again for unregister user and existing in email table
def test_to_send_token(client,created_email):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/emails/",json= email)
    token = schema.VerifyToken(**res.json())
    print(token)
    assert res.status_code == 201

# authorized client registering in user account
def test_authorized_client_to_register(authorized_client):
    user_data = {"first_name":"ganesh","last_name":"chelluri","phone_number":9876543210,"password":"password"}
    res = authorized_client.post("/users/register",json= user_data)
    assert res.status_code == 201

# authorized client registering in user account again
def test_authorized_client_trying_to_register_again(authorized_client):
    authorized_client.headers["Authorization"]="None"
    user_data = {"first_name":"ganesh","last_name":"chelluri","phone_number":9876543210,"password":"password"}
    res = authorized_client.post("/users/register",json= user_data)
    print(res.json())
    assert res.status_code == 401

# unauthorized client registering in user account
def test_unauthorized_client_trying_to_register(client):
    client.headers["Authorization"]="Incorrect Token"  # api requires a token from header
    user_data = {"first_name":"ganesh","last_name":"chelluri","phone_number":9876543210,"password":"password"}
    res = client.post("/users/register",json= user_data)
    print(res.json())
    assert res.status_code == 401

# existing user creating email again
def test_pre_existing_user_creating_email(client,registered_user):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/emails/",json=email)
    print(res.json())
    assert res.status_code == 226