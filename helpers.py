import requests 
from secrets import YELP_API_SECRET_KEY, GEOCODE_API_KEY

BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def get_geocode_location(address):
    """This function is to help get the longitude and latitude of an address entered into the dateMeet app"""

    resp = requests.get(f"{BASE_URL}?address={address}&key={GEOCODE_API_KEY}")

    long = resp["results"][0]["geometry"]["location"]["lng"]
    lat = resp["resulta"][0]["geometry"]["location"]["lat"]
    full_addy = resp["results"][0]["formatted_address"]

    location = {
        "full_address": full_addy,
        "longitude": long,
        "latitude": lat
    }

    return location