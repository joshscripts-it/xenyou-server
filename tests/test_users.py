from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user

client = TestClient(app)

def test_create_user():
    user_data = {"username": "testuser", "email": "testuser@example.com", "password": "password123"}
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["username"] == user_data["username"]
    assert created_user["email"] == user_data["email"]

def test_get_user():
    user_data = {"username": "testuser2", "email": "testuser2@example.com", "password": "password123"}
    create_user(UserCreate(**user_data))
    
    response = client.get("/api/v1/users/testuser2")
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["username"] == user_data["username"]
    assert retrieved_user["email"] == user_data["email"]

def test_create_user_invalid_email():
    user_data = {"username": "testuser3", "email": "invalid-email", "password": "password123"}
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422

def test_get_nonexistent_user():
    response = client.get("/api/v1/users/nonexistentuser")
    assert response.status_code == 404