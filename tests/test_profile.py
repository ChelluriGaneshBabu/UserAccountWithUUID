# authorized user creating profile
def test_authorized_user_create_profile(authorized_user):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"M-tech"}
    res = authorized_user.post("/profile/",json= data)
    assert res.status_code == 201

# unauthorized user creating profile
def test_unauthorized_user_create_profile(client,registered_user_2):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"M-tech"}     
    res = client.post("/profile/",json=data)
    assert res.status_code == 401

# authorized user creating profile again
def test_authorized_user_create_profile_again(authorized_user,create_user_2_profile):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"M-tech"}
    res = authorized_user.post("/profile/",json = data)
    assert res.status_code == 403

# authorized user editing profile
def test_authorized_user_edit_profile(authorized_user,create_user_2_profile):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"b-tech"}
    res = authorized_user.put("/profile/edit_profile",json= data)
    print(res.json())
    assert res.status_code == 200

# unauthorized user editing profile
def test_unauthorized_user_edit_profile(client,create_user_2_profile):
    client.headers["Authorization"]="None"
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"b-tech"}
    res = client.put("/profile/edit_profile",json= data)
    print(res.json())
    assert res.status_code == 401

# authorized user editing profile which does not exist
def test_authorized_user_edit_profile(authorized_user):
    data = {"date_of_birth":"1999-08-16","address":"vijaynagaram","highest_qualification":"b-tech"}
    res = authorized_user.put("/profile/edit_profile",json= data)
    print(res.json())
    assert res.status_code == 404