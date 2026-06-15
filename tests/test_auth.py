from utils import generate_booking_payload
from models import Auth
from clients import BookingClient


def test_auth_token(auth_token):
    token = Auth(token=auth_token)
    assert isinstance(token.token, str)


def test_delete_booking(auth_token):
    client = BookingClient()
    data = generate_booking_payload()
    booking_id = client.create_booking(data)
    booking_del = client.delete_booking(booking_id, auth_token)
    assert booking_del.status_code == 201


