import requests
import json
from config_data.config import RAPID_API_KEY

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def find_city(city_name: str) -> list:
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city_name, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    response = requests.get(url=url, headers=headers, params=querystring)
    data = json.loads(response.text)

    cities = list()
    for indexes in data['sr']:
        cities.append(indexes['regionNames']['fullName'])
    return cities
