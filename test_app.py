import os
import pytest
from app import app, init_db, get_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_home_page(client):
    """Test user-facing homepage responds with 200 OK and contains brand text."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"ParkSmart" in response.data
    assert b"Live Parking Matrix" in response.data

def test_admin_dashboard(client):
    """Test admin dashboard responds with 200 OK and metrics."""
    response = client.get("/admin")
    assert response.status_code == 200
    assert b"Parking Operations & Occupancy" in response.data
    assert b"Total Capacity" in response.data

def test_api_slots_listing(client):
    """Test /api/slots returns valid JSON list of slots."""
    response = client.get("/api/slots")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] >= 20
    assert len(data["slots"]) >= 20

def test_api_stats(client):
    """Test /api/stats returns numerical metrics for dashboard."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "total" in data
    assert "available" in data
    assert "revenue" in data

def test_reserve_and_release_workflow(client):
    """Test complete reservation lifecycle: reserve bay -> verify -> release bay."""
    # Find an available slot
    slots_res = client.get("/api/slots?status=available")
    available_slots = slots_res.get_json()["slots"]
    assert len(available_slots) > 0
    target_slot = available_slots[0]["slot_number"]

    # 1. Reserve slot
    booking_payload = {
        "slot_number": target_slot,
        "vehicle_number": "TN-37-TEST-9999",
        "driver_name": "Test Driver",
        "phone": "9999988888",
        "vehicle_type": "Car",
        "expected_hours": 3
    }
    reserve_res = client.post("/api/reserve", json=booking_payload)
    assert reserve_res.status_code == 200
    res_data = reserve_res.get_json()
    assert res_data["success"] is True
    res_code = res_data["reservation"]["reservation_code"]
    assert res_code.startswith("PKG-")

    # 2. Verify slot is now reserved
    slots_check = client.get(f"/api/slots")
    slot_obj = next((s for s in slots_check.get_json()["slots"] if s["slot_number"] == target_slot), None)
    assert slot_obj is not None
    assert slot_obj["status"] == "reserved"

    # 3. Release slot using reservation code
    release_payload = {"identifier": res_code}
    release_res = client.post("/api/release", json=release_payload)
    assert release_res.status_code == 200
    rel_data = release_res.get_json()
    assert rel_data["success"] is True

    # 4. Verify slot is available again
    slots_check2 = client.get("/api/slots")
    slot_obj2 = next((s for s in slots_check2.get_json()["slots"] if s["slot_number"] == target_slot), None)
    assert slot_obj2 is not None
    assert slot_obj2["status"] == "available"

def test_reserve_invalid_slot(client):
    """Test reserving a non-existent slot returns 404."""
    payload = {
        "slot_number": "Z-99",
        "vehicle_number": "TN-37-ZZ-0000",
        "driver_name": "Invalid Guy",
        "phone": "9000000000",
        "vehicle_type": "Car",
        "expected_hours": 1
    }
    response = client.post("/api/reserve", json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False

def test_release_invalid_identifier(client):
    """Test releasing non-existent reservation code returns 404."""
    payload = {"identifier": "NON-EXISTENT-CODE"}
    response = client.post("/api/release", json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data["success"] is False
