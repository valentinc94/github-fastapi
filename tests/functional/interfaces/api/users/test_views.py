from unittest import mock

from fastapi.testclient import TestClient
from tests.fixtures import load_fixture
from vendors.auth import InvalidCredentials, UnableToUpdateUserData
from vendors.main import app

client = TestClient(app)


@mock.patch("vendors.auth.GithubAPI.get_user_data")
def test_auth_user_with_github_return_success(mock_get_user_data):
    data = load_fixture("github_auth_message.json")
    mock_get_user_data.return_value = data
    response = client.post(url="/user/login/", json={"token": "1234"})
    user_data = response.json()
    assert response.status_code == 200
    assert user_data["user_data"]["id"] == data["id"]
    assert user_data["user_data"]["login"] == data["login"]
    assert mock_get_user_data.called


@mock.patch("vendors.auth.GithubAPI.get_user_data")
def test_auth_user_with_github_return_invalid_credentials(mock_get_user_data):
    mock_get_user_data.side_effect = InvalidCredentials()
    response = client.post(url="/user/login/", json={"token": "1234"})
    user_data = response.json()
    assert response.status_code == 400
    assert user_data["code_transaction"] == "INVALID_CREDENTIALS"
    assert user_data["message"] == "Invalid Credentials."
    assert mock_get_user_data.called


@mock.patch("vendors.auth.GithubAPI.edit_user_data")
def test_edit_user_with_github_return_success(mock_edit_user_data):
    data = load_fixture("github_auth_message.json")
    mock_edit_user_data.return_value = data
    response = client.put(
        url="/user/update/",
        json={
            "auth": {"token": "1"},
            "user": {"bio": "hello"},
        },
    )
    user_data = response.json()
    assert response.status_code == 200
    assert user_data["user_data"]["id"] == data["id"]
    assert user_data["user_data"]["login"] == data["login"]
    assert mock_edit_user_data.called


@mock.patch("vendors.auth.GithubAPI.edit_user_data")
def test_edit_user_with_github_return_invalid_credentials(mock_edit_user_data):
    mock_edit_user_data.side_effect = InvalidCredentials()
    response = client.put(
        url="/user/update/",
        json={
            "auth": {"token": "1"},
            "user": {"bio": "hello"},
        },
    )
    user_data = response.json()
    assert response.status_code == 400
    assert user_data["code_transaction"] == "INVALID_CREDENTIALS"
    assert user_data["message"] == "Invalid Credentials."
    assert mock_edit_user_data.called


@mock.patch("vendors.auth.GithubAPI.edit_user_data")
def test_edit_user_with_github_return_unable_to_update(mock_edit_user_data):
    mock_edit_user_data.side_effect = UnableToUpdateUserData("invalid_format")
    response = client.put(
        url="/user/update/",
        json={
            "auth": {"token": "1"},
            "user": {"bio": "hello"},
        },
    )
    user_data = response.json()
    assert response.status_code == 400
    assert user_data["code_transaction"] == "UNABLE_TO_UPDATE_RECORD"
    assert user_data["message"] == "Invalid input data invalid_format."
    assert mock_edit_user_data.called
