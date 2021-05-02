import requests 
from secrets import YELP_API_SECRET_KEY, GEOCODE_API_KEY

business_num = 0

def get_lat_lng(apiKey, address):
    """
    This method Returns the latitude and longitude of a location using the Google Maps Geocoding API. 
    API: https://developers.google.com/maps/documentation/geocoding/start

    # INPUT -------------------------------------------------------------------
    apiKey                  [str]
    address                 [str]

    # RETURN ------------------------------------------------------------------
    location = {
        "full_address": addy      [str],
        "latitude": lat           [float],
        "longitude": lng          [float]
    }
    """
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
           .format(address.replace(' ','+'), apiKey))
    try:
        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        addy = resp_json_payload['results'][0]['formatted_address']
        address_components = resp_json_payload['results'][0]['address_components']

        if len(address_components) == 8: 
            city = address_components[3]['short_name']
            state = address_components[5]['short_name']
        else:
            city = address_components[3]['short_name']
            state = address_components[4]['short_name']

    except:
        # print('ERROR: {}'.format(address))
        lat = 0
        lng = 0
        addy = address
        city = "city"
        state = "state"

    location = {
        "full_address": addy,
        "latitude": lat,
        "longitude": lng,
        "city": city,
        "state": state
    }

    
    return location


def yelp_business_search(apikey, address, term):
    """This method makes the request to the Yelp API to retrieve businesses
        around a specific location given the address.

        API:https://www.yelp.com/developers/documentation/v3/business_search

        # INPUT ---------------------------------------------------------------
        apikey               [str]
        address              [str]
        term                 [str]

        #RETURN ----------------------------------------------------------------
        YELP RESPONSE SHOWN IN BUSINESS SEARCH DOCUMENTATION:
        https://www.yelp.com/developers/documentation/v3/business_search

    """
# Define endpoint and header
    ENDPOINT = "https://api.yelp.com/v3/businesses/search"
    HEADERS = {'Authorization': 'bearer %s' %apikey}

# Define the parameters 
    PARAMS = {'term': term,
              'limit': 50,
              'radius': 40000,
              'offset': 50,
            #   'open_now': True,
              'location': address}

# Now we make the request to the Yelp API

    response = requests.get(url=ENDPOINT, params=PARAMS, headers=HEADERS)

# Convert JSON response to dictionary

    business_data = response.json()

    # print (business_data.keys())

    return {"businesses":[{
            'name': biz['name'],
            'yelp_url': biz['url'],
            'phone_num': biz['phone'],
            'rating': biz['rating'],
            'image_url': biz['image_url'],
            'yelp_id': biz['id'],
            'coordinates': biz['coordinates'],
            'location': biz['location'],
            'is_closed':biz['is_closed']
            }
         for biz in business_data["businesses"]]}


# def yelp_business_match(apikey, name, address):
#     """This method makes the request to the Yelp API to retrieve a 
#         particular business given the business name and address.

#         API:https://www.yelp.com/developers/documentation/v3/business_match

#         # INPUT ---------------------------------------------------------------
#         apikey               [str]
#         name                 [str]
#         address              [str]

#         #RETURN ----------------------------------------------------------------
#         YELP RESPONSE SHOWN IN BUSINESS SEARCH DOCUMENTATION:
#         https://www.yelp.com/developers/documentation/v3/business_match

#     """
# # Define endpoint and header
#     ENDPOINT = "https://api.yelp.com/v3/businesses/matches"
#     HEADERS = {'Authorization': 'bearer %s' %apikey}

# # Define the parameters 
#     PARAMS = {'term': term,
#               'limit': 50,
#               'radius': 40000,
#               'offset': 50,
#             #   'open_now': True,
#               'location': address}

# # Now we make the request to the Yelp API

#     response = requests.get(url=ENDPOINT, params=PARAMS, headers=HEADERS)

# # Convert JSON response to dictionary

#     business_data = response.json()

#     # print (business_data.keys())

#     return {"businesses":[{
#             'name': biz['name'],
#             'yelp_url': biz['url'],
#             'phone_num': biz['phone'],
#             'rating': biz['rating'],
#             'image_url': biz['image_url'],
#             'yelp_id': biz['id'],
#             'coordinates': biz['coordinates'],
#             'location': biz['location'],
#             'is_closed':biz['is_closed']
#             }
#          for biz in business_data["businesses"]]}
        