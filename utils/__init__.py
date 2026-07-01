from faker import Faker
from datetime import timedelta, date

fake = Faker()

def generate_booking_payload():
    
    checkin = fake.date_between(start_date="+1d", end_date="+30d")
    checkout = fake.date_between(start_date=checkin + timedelta(days=1), end_date=checkin + timedelta(days=13))
    booking_data = {
    "firstname": fake.first_name(),
    "lastname": fake.last_name(),
    "totalprice": fake.random_int(min=100, max=1000),
    "depositpaid": True,
    "bookingdates": {
        "checkin": checkin.strftime("%Y-%m-%d"),
        "checkout": checkout.strftime("%Y-%m-%d")
    },
    "additionalneeds": fake.sentence()
    }
    
    return booking_data
    
