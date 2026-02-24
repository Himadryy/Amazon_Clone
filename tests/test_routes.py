import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User, Product


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_get_products(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.get_json()
    assert "products" in data


def test_get_categories(client):
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.get_json()
    assert "categories" in data


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_signin_page(client):
    response = client.get("/auth/signin")
    assert response.status_code == 200


def test_signup_page(client):
    response = client.get("/auth/signup")
    assert response.status_code == 200
