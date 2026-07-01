from utils import generate_booking_payload
from models import Auth, Booking
from clients import BookingClient
from datetime import date
import pytest


def test_auth_token(auth_token):
    token = Auth(token=auth_token)
    assert isinstance(token.token, str)


def test_delete_booking(auth_token):
    client = BookingClient()
    data = generate_booking_payload()
    booking_id = client.create_booking(data)
    booking_del = client.delete_booking(booking_id, auth_token)
    assert booking_del.status_code == 201


def test_get_booking(booking):
    client = BookingClient()
    booking_id, expected = booking

    response = client.get_booking(booking_id)

    assert response.status_code == 200
    body = Booking(**response.json())
    actual = body.model_dump(mode="json")

    assert actual == expected


@pytest.mark.parametrize("field, value", [
    ("firstname", "Alice"),
    ("lastname", "Morgan"),
    ("totalprice", 999)
])
def test_patch_booking(booking, auth_token, field, value):
    client = BookingClient()
    booking_id, before = booking
    patch = {field: value}
    resp = client.patch_booking(booking_id, patch, auth_token)
    
    assert resp.status_code == 200
    
    get_resp = client.get_booking(booking_id)
    after = Booking(**get_resp.json())
    actual = after.model_dump(mode="json")

    assert actual[field] == value
    for key in before:
        if key != field:
            assert actual[key] == before[key]


def test_put_booking(booking, auth_token):
    client = BookingClient()
    booking_id, _ = booking
    new_payload = generate_booking_payload()
    response = client.put_booking(booking_id, new_payload, auth_token)
    
    assert response.status_code == 200
    
    get_resp = client.get_booking(booking_id)
    after = Booking(**get_resp.json())
    after_dict = after.model_dump(mode="json")
    
    assert new_payload == after_dict
