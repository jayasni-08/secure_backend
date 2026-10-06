def test_normal_user_cannot_get_all_users(client):
    client.post(
        "/auth/register",
        json={
            "username": "normaluser",
            "password": "Test@12345"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": "normaluser",
            "password": "Test@12345"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_user_can_access_own_profile(client):
    client.post(
        "/auth/register",
        json={
            "username": "profileuser",
            "password": "Test@12345"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "username": "profileuser",
            "password": "Test@12345"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "profileuser"
    assert data["role"] == "user"