from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def get_year():
    """
    gets year from the user
    :(None)
    :return: year - (int)
    """
    print("please, enter the year from 1890-2024.")
    prompt = input()
    while 1:
        if int(prompt) not in range(1890, 2025):
            print("enter valid year.")
            prompt = input()
        else:
            prompt = int(prompt)
            break

    return prompt


def get_user_location():
    """
    asks user to enter their location
    :return: two float numbers, representing latitude and longitude
    """
    usr_loc = input("enter your city: ")
    location = geolocator.geocode(usr_loc, timeout=10)
    while 1:
        if location:
            break
        else:
            print("enter a valid city name: ")
            usr_loc = input("enter your city: ")
            location = geolocator.geocode(usr_loc, timeout=10)

    return location
