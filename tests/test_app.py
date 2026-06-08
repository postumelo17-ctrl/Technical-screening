import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestCalculateEndpoint:
    def test_calculate_basic(self):
        """Test basic calculation"""
        response = client.post("/calculate", json={"amount": 100000, "rate": 0.05})
        assert response.status_code == 200
        assert "monthly" in response.json()
        assert abs(response.json()["monthly"] - 416.67) < 1

    def test_calculate_zero_rate(self):
        """Test calculation with zero rate"""
        response = client.post("/calculate", json={"amount": 100000, "rate": 0})
        assert response.status_code == 200
        assert response.json()["monthly"] == 0

    def test_calculate_decimal_precision(self):
        """Test decimal precision"""
        response = client.post("/calculate", json={"amount": 1000, "rate": 0.15})
        assert response.status_code == 200
        expected = (1000 * 0.15) / 12
        assert response.json()["monthly"] == expected

    def test_calculate_missing_amount(self):
        """Test error handling for missing amount"""
        response = client.post("/calculate", json={"rate": 0.05})
        assert response.status_code == 422

    def test_calculate_missing_rate(self):
        """Test error handling for missing rate"""
        response = client.post("/calculate", json={"amount": 100000})
        assert response.status_code == 422

class TestHealthEndpoint:
    def test_health_returns_200(self):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_contains_status(self):
        """Test health check contains status"""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_health_contains_timestamp(self):
        """Test health check contains valid timestamp"""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
        assert len(data["timestamp"]) > 0
