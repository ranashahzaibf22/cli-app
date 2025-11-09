"""Tests for product endpoints"""
import pytest
from fastapi import status


def test_create_product(client, test_user_data, test_product_data):
    """Test creating a product"""
    # Register and login to get token
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    
    # Create product
    response = client.post(
        "/api/v1/products/",
        json=test_product_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == test_product_data["name"]
    assert data["price"] == test_product_data["price"]


def test_get_products(client, test_user_data, test_product_data):
    """Test getting products list"""
    # Create a product first
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    client.post(
        "/api/v1/products/",
        json=test_product_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get products
    response = client.get("/api/v1/products/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_product_by_id(client, test_user_data, test_product_data):
    """Test getting product by ID"""
    # Create a product first
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    create_response = client.post(
        "/api/v1/products/",
        json=test_product_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    product_id = create_response.json()["id"]
    
    # Get product
    response = client.get(f"/api/v1/products/{product_id}")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == test_product_data["name"]


def test_get_categories(client):
    """Test getting product categories"""
    response = client.get("/api/v1/products/categories")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
