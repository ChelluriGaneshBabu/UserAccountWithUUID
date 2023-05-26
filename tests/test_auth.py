import pytest

# registerd user trying to login
def test_registered_user_login(client,registered_user):
    login_data = {"username":"ganesh@gmail.com","password":"password"}
    res= client.post("/login",data=login_data) # use data because the data is not in json format
    assert res.status_code == 201

# unregistered user trying to login
def test_unregistered_user_login(client,registered_user):
    login_data = {"username":"unregistered@gmail.com","password":"password"}
    res = client.post("/login",data = login_data)
    assert res.status_code == 404

# logging with incorrect credentials
@pytest.mark.parametrize("username,password,status_code",[
                         ("ganesh@gmail.com","wrongpassword",403),
                         ("unregistered@gmail.com","password",404),
                         (None,"password",422),
                         ("ganesh@gmail.com",None,422)
                        ])
def test_incorrect_user_login(client,registered_user,username,password,status_code):
    login_data = {"username":username,"password":password}
    res = client.post("/login",data = login_data)
    assert res.status_code == status_code