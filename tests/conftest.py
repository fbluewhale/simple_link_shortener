import pytest, sys, os
from fastapi.testclient import TestClient
from pymongo import MongoClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from src.app import app

# Adjust import path as per your project structure


# Example MongoDB connection for testing
@pytest.fixture(scope="session")
def test_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["link_shortener_test"]
    yield db
    client.drop_database("link_shortener_test")


# Fixture for FastAPI test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client
