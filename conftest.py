import pytest
from config import USERNAME, PASSWORD
from clients import BookingClient
from utils import generate_booking_payload


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
    data = generate_booking_payload()
    booking_id = client.create_booking(data)
    yield booking_id, data
    client.delete_booking(booking_id, auth_token)

    
