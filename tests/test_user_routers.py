from beanie import PydanticObjectId
from database.models import User # мои Document-модели


### === Тесты для user_routers.py === ###

# == Минимальная схема тестов == #

# POST
# ├── success ✅
# ├── invalid age ✅
# ├── empty name ✅
# └── notes > 5 ✅

# GET
# ├── success ✅
# ├── invalid ObjectId → 422 ✅
# └── valid ObjectId, user doesn't exist → 404 ✅

# PATCH
# ├── update one field ✅
# ├── update several fields ❌
# ├── invalid data → 422 ✅
# ├── invalid ObjectId → 422 ✅
# └── valid ObjectId, user doesn't exist → 404 ✅

# DELETE
# ├── success ✅
# ├── invalid ObjectId → 422 ✅
# └── valid ObjectId, user doesn't exist → 404 ✅

async def test_create_user(app_client):
    res = await app_client.post("/users", json={
        "name": "John",
        "surname": "Doe",
        "age": 25,
        "notes": ["Note 1", "Note 2"]
    })

    assert res.status_code == 201
    assert res.json()["first_name"] == "John"
    assert res.json()["last_name"] == "Doe"
    assert res.json()["age"] == 25
    assert res.json()["notes"] == ["Note 1", "Note 2"]

async def test_create_user_invalid_age(app_client):
    res = await app_client.post("/users", json={
        "name": "John",
        "surname": "Doe",
        "age": -1,
        "notes": ["Note 1", "Note 2"]
    })

    assert res.status_code == 422

async def test_create_user_empty_name(app_client):
    res = await app_client.post("/users", json={
        "name": "",
        "surname": "Doe",
        "age": 25,
        "notes": ["Note 1", "Note 2"]
    })

    assert res.status_code == 422

async def test_create_user_notes_more_than_5(app_client):
    res = await app_client.post("/users", json={
        "name": "John",
        "surname": "Doe",
        "age": 25,
        "notes": ["Note 1", "Note 2", "Note 3", "Note 4", "Note 5", "Note 6"]
    })

    assert res.status_code == 422

async def test_get_user(app_client):
    user = User(first_name="John", last_name="Doe", age=25, notes=["Note 1", "Note 2"])
    await user.insert()

    res = await app_client.get(f"/users/{user.id}")

    assert res.status_code == 200
    assert res.json()["first_name"] == "John"
    assert res.json()["last_name"] == "Doe"
    assert res.json()["age"] == 25
    assert res.json()["notes"] == ["Note 1", "Note 2"]

async def test_get_nonexistent_user(app_client):
    res = await app_client.get("/users/123")

    assert res.status_code == 422

async def test_get_nonexistent_user_404(app_client):
    user_id = PydanticObjectId()

    res = await app_client.get(f"/users/{user_id}")

    assert res.status_code == 404

async def test_patch_user(app_client):
    user = User(first_name="John", last_name="Doe", age=25, notes=["Note 1", "Note 2"])
    await user.insert()

    res = await app_client.patch(f"/users/{user.id}", json={
        "age": 30,
        "notes": ["Note 3", "Note 4"]
    })

    assert res.status_code == 200
    assert res.json()["first_name"] == "John"
    assert res.json()["last_name"] == "Doe"
    assert res.json()["age"] == 30
    assert res.json()["notes"] == ["Note 3", "Note 4"]

async def test_patch_nonexistent_user(app_client):
    res = await app_client.patch("/users/123", json={
        "age": 30,
        "notes": ["Note 3", "Note 4"]
    })

    assert res.status_code == 422

async def test_patch_nonexistent_user_404(app_client):
    user_id = PydanticObjectId()

    res = await app_client.patch(
        f"/users/{user_id}",
        json={
            "age": 30,
            "notes": ["Note 3", "Note 4"]
        }
    )

    assert res.status_code == 404

async def test_delete_user(app_client):
    user = User(first_name="John", last_name="Doe", age=25, notes=["Note 1", "Note 2"])
    await user.insert()

    res = await app_client.delete(f"/users/{user.id}")

    assert res.status_code == 200

    res = await app_client.get(f"/users/{user.id}")
    assert res.status_code == 404


async def test_delete_nonexistent_user(app_client):
    res = await app_client.delete("/users/123")

    assert res.status_code == 422

async def test_delete_nonexistent_user_404(app_client):
    user_id = PydanticObjectId()

    res = await app_client.delete(f"/users/{user_id}")

    assert res.status_code == 404


