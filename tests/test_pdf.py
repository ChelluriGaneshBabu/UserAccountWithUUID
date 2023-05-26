# authorized user generating pdf
def test_authorized_user_generating_pdf(authorized_user,create_user_2_profile):
    res = authorized_user.get("/profile_to_pdf")
    assert res.status_code == 200

# unauthorized user generating pdf
def test_unauthorized_user_generating_pdf(client,create_user_2_profile):
    client.headers["Authorization"] = "none"
    res = client.get("/profile_to_pdf")
    assert res.status_code == 401

# authorized user generating pdf which does not exist
def test_authorized_user_generating_pdf_which_not_exist(authorized_user,registered_user_2):
    res = authorized_user.get("/profile_to_pdf")
    assert res.status_code == 404