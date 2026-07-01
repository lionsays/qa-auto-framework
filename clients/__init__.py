from config import BASE_URL
import requests
from requests import Response

class BookingClient:
    
    def __init__(self):
        self.base_url = BASE_URL

    def get_bookings(self):
        response = requests.get(f"{self.base_url}/booking")
        return response
    
    def get_booking(self, booking_id: int):
        response = requests.get(f"{self.base_url}/booking/{booking_id}")
        return response
    
    def get_auth(self, data):
        response = requests.post(f"{BASE_URL}/auth", json=data)
        token = response.json()["token"]
        return token

    def create_booking(self, data):
        response = requests.post(f"{BASE_URL}/booking", json=data)
        booking_id = response.json()["bookingid"]
        return booking_id
    
    def delete_booking(self, booking_id: str, token: str):
        headers = {"Cookie": f"token={token}"}
        booking_del = requests.delete(f"{self.base_url}/booking/{booking_id}", headers=headers)
        return booking_del

    def patch_booking(self, booking_id: int, payload: dict, token: str) -> Response:
        headers = {
            "Cookie": f"token={token}"
            }
        response = requests.patch(f"{self.base_url}/booking/{booking_id}", headers=headers, json=payload)
        return response
    
    def put_booking(self, booking_id: int, payload: dict, token: str) -> Response:
        headers = {
            "Cookie": f"token={token}"
        }
        response = requests.put(f"{self.base_url}/booking/{booking_id}", headers=headers, json=payload)
        return response