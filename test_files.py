from io import BytesIO


def get_token(client):
    client.post(
        "/auth/register",
        json={
            "username": "fileuser",
            "password": "Test@12345"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": "fileuser",
            "password": "Test@12345"
        }
    )

    return response.json()["access_token"]


def test_upload_file(client):
    token = get_token(client)

    response = client.post(
        "/files/upload",
        headers={
            "Authorization": f"Bearer {token}"
        },
        files={
            "uploaded_file": (
                "test.txt",
                BytesIO(b"Hello secure backend"),
                "text/plain"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "test.txt"
    assert "id" in data


def test_list_files_requires_authentication(client):
    response = client.get("/files/")

    assert response.status_code in [401, 403]