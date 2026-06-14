import pytest
from config import USERNAME, PASSWORD
from clients import BookingClient


@pytest.fixture(scope="session")
def auth_token():
    data = {
        "username": USERNAME, 
        "password": PASSWORD
        }

    client = BookingClient()
    token = client.get_auth(data)
    return token

@pytest.fixture
def booking(auth_token):
    client = BookingClient()
    data = {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-01-01",
        "checkout": "2025-01-10"
        },
    "additionalneeds": "Breakfast"
    }
    booking_id = client.create_booking(data)
    yield booking_id
    client.delete_booking(booking_id, auth_token)

    