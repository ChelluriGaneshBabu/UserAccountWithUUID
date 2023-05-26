import pytest

# authorized user changing password
def test_authorized_user_change_password(authorized_user):
    password_data = {"old_password":"password","new_password":"password123"}
    res = authorized_user.put("/users/change_password",json=password_data)
    print(res.json())
    assert res.status_code == 200

# unauthorized user changing password
def test_unauthorized_user_change_password(client,registered_user):
    password_data = {"old_password":"password","new_password":"password123"}
    res = client.put("/users/change_password",json=password_data)
    assert res.status_code == 401

# authorized user changing password by entering wrong passwords
@pytest.mark.parametrize("old_password,new_password,status_code",[
    ("wrongpassword","password123",403),
    ("password",None,422),
    (None,"password123",422)
])
def test_authorized_user_change_password(authorized_user,old_password,new_password,status_code):
    password_data = {"old_password":old_password,"new_password":new_password}
    res = authorized_user.put("/users/change_password",json=password_data)
    assert res.status_code == status_code

# registered user forget password
def test_registered_user_forget_password(client,registered_user):
    email = {"user_email":"ganesh@gmail.com"}
    res = client.post("/users/forget_password",json=email)
    assert res.status_code == 201

# unregistered user forget password
def test_registered_user_forget_password(client,registered_user,registered_user_2):
    email = {"user_email":"banu@gmail.com"}
    res = client.post("/users/forget_password",json=email)
    assert res.status_code == 404

# authorized user who forget password setting password
def test_authorized_user_set_new_password(authorized_user_who_forget_password):
    password = {"new_password":"password123"}
    res = authorized_user_who_forget_password.put("/users/set_new_password",json= password)
    print(res.json())
    assert res.status_code == 200

# unauthorized user who forget password setting password
def test_unauthorized_user_set_new_password(client,registered_user):
    # client.headers= {**client.headers,"Authorization":"None"}
    client.headers["Authorization"]="None"
    password = {"new_password":"password123"}
    res = client.put("/users/set_new_password",json= password)
    print(res.json())
    assert res.status_code == 401