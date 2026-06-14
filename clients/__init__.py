from config import BASE_URL
import requests
from models.booking import Booking

class BookingClient:
    
    def __init__(self):
        self.base_url = BASE_URL

    def get_bookings(self):
        response = requests.get(f"{self.base_url}/booking")
        return response
    
    def get_booking(self, booking_id: int):
        response = requests.get(f"{self.base_url}/booking/{booking_id}")
        data = response.json()
        return Booking(**data)
    
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
