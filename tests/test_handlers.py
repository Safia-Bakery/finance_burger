import os
import sys
from datetime import datetime
from core.config import timezonetash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import json
# from .conftest import client, get_user_from_database


async def test_create_user(client, get_user_from_database):
    user_data = {
        "tg_id": 1618364630,
        "fullname": "Bakhtiyor Bakhriddinov",
        "language": "ru",
        "phone": "+998977873422",
        "username": "dsdfs",
        "password": "asd323",
        "location": {"lang": 1231.435, "long": 23212.453},
        "email": "dataeng27@gmail.com"
    }
    # response = await client.post("/users/", data=json.dumps(user_data))
    response = await client.post("/users/", json=user_data)
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["tg_id"] == user_data["tg_id"]
    assert response_data["fullname"] == user_data["fullname"]
    assert response_data["language"] == user_data["language"]
    assert response_data["phone"] == user_data["phone"]
    users_from_db = await get_user_from_database(response_data["id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["tg_id"] == user_data["tg_id"]
    assert user_from_db["fullname"] == user_data["fullname"]
    assert user_from_db["language"] == user_data["language"]
    assert user_from_db["phone"] == user_data["phone"]
    assert str(user_from_db["id"]) == str(response_data["id"])

