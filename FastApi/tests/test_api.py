import pytest
from fastapi.testclient import TestClient

from main import app
from services.restaurantService import get_restaurant_service

client = TestClient(app)

class DummyRestaurantService:
    async def list_restaurants(self, limit, offset, name, address):
        return []
        
    async def search_restaurants(self, query, limit, offset):
        return []

    async def get_restaurant_detail(self, id):
        return None

def override_get_restaurant_service():
    return DummyRestaurantService()

app.dependency_overrides[get_restaurant_service] = override_get_restaurant_service


def test_healthz():

    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_restaurants_endpoint():

    response = client.get("/api/v1/restaurants/")
    assert response.status_code == 200
    assert response.json() == []


def test_search_restaurants_endpoint():

    response = client.get("/api/v1/restaurants/search/?query=Pizza")
    assert response.status_code == 200
    assert response.json() == []

def test_search_restaurants_validation_error():

    response = client.get("/api/v1/restaurants/search/")
    assert response.status_code == 422


def test_get_restaurant_detail_not_found():

    from uuid import uuid4
    fake_id = str(uuid4())
    response = client.get(f"/api/v1/restaurants/{fake_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "restaurant not found"}
