from pydantic import BaseModel
import pytest
import requests


class AccessTokenRequest(BaseModel):
    access_token: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str


def test_access_token_required():
    request = {
        "access_token": "fdkvnfk54865"
    }
    AccessTokenRequest(**request)


def test_users_get_response():
    response = [
        {"id": 475138907, "first_name": "Liza", "last_name": "Darina"},
        {"id": 745213994, "first_name": "Andrey", "last_name": "Borisov"}
    ]
    users = [User(**user) for user in response]


def test_access_token_required():
    request = {}
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_access_token_format():
    request = {
        "access_token": "invalid_token_format"
    }
    with pytest.raises(ValueError):
        AccessTokenRequest(**request)


def test_users_get_success():
    response = [
        {"id": 475138907, "first_name": "Liza", "last_name": "Darina"},
        {"id": 745213994, "first_name": "Andrey", "last_name": "Borisov"}
    ]
    users = [User(**user) for user in response]
    assert len(users) == 2
    assert users[1].id == 745213994
    assert users[1].first_name == "Andrey"
    assert users[1].last_name == "Borisov"


def test_users_get_no_users():
    response = []
    users = [User(**user) for user in response]
    assert len(users) == 0


def test_user_format():
    user = {
        "id": "invalid_user_id",
        "first_name": "Liza",
        "last_name": "Darina"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_name_format():
    user = {
        "id": 475138907,
        "first_name": "Liza111",
        "last_name": "Darina"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_user_lastname_format():
    user = {
        "id": 475138907,
        "first_name": "Liza",
        "last_name": "Darina111"
    }
    with pytest.raises(ValueError):
        User(**user)


def test_users_get_one_user():
    response = [{"id": 475138907, "first_name": "Liza", "last_name": "Darina"}]
    users = [User(**user) for user in response]
    assert len(users) == 1
    assert users[0].id == 475138907
    assert users[0].first_name == "Liza"
    assert users[0].last_name == "Darina"


def test_users_get_max_users():
    response = [{"id": i, "first_name": "User", "last_name": str(i)} for i in range(100000)
                ]
    users = [User(**user) for user in response]
    assert len(users) == 100000
    assert users[-1].id == 99999
    assert users[-1].first_name == "User"
    assert users[-1].last_name == "99999"


def test_users_get_invalid_response():
    response = [{"invalid_attr": "value"}]
    with pytest.raises(ValueError):
        users = [User(**user) for user in response]