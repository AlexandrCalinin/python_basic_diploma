import requests
import re
import json
from config_data.config import RAPID_API_KEY

headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def find_city(city_name):
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": city_name, "locale": "ru_RU", "currency": "RUB"}
    response = requests.request("GET", url=url, headers=headers, params=querystring)
    pattern = r'(?<="CITY_GROUP",)_+?[\]]'
    find = re.search(pattern, response.text)
    cities = list()

    if find:
        suggestions = json.loads(f'{{{find[0]}}}')
        for id in suggestions['entities']:
            cities.append({'city_name': id['name'], 'destination_id': id['destinationId']})
    return cities
