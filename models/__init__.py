from pydantic import BaseModel
from models.booking import Booking, BookingDates


class Auth(BaseModel):
    token: str