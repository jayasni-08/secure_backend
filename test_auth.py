def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert "id" in data


def test_login(client):
    client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "password": "Test@12345"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "loginuser",
            "password": "Test@12345"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "wronguser",
            "password": "Wrong@12345"
        }
    )

    assert response.status_code == 401