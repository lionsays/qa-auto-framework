import requests
from config import BASE_URL
from models import Auth
from clients import BookingClient


def test_auth_token(auth_token):
    token = Auth(token=auth_token)
    assert isinstance(token.token, str)


def test_delete_booking(booking, auth_token):
    client = BookingClient()
    

    booking_del = client.delete_booking(booking, auth_token)

    assert booking_del.status_code == 201


