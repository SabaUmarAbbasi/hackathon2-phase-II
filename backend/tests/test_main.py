import pytest
from fastapi.testclient import TestClient
from backend.src.main import app
from backend.src.database.database import engine, get_session
from backend.src.models.user import User
from sqlmodel import SQLModel, Session, select
from backend.src.auth.auth import get_password_hash

# Create a test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Test the root endpoint
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Todo API"}

# Test user registration
def test_register_user(client):
    # First, clean up any existing test user
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if existing_user:
            session.delete(existing_user)
            session.commit()
    
    # Register a new user
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

# Test user login
def test_login_user(client):
    # Register a user first
    client.post(
        "/api/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpassword"
        }
    )
    
    # Login with the registered user
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login_test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"