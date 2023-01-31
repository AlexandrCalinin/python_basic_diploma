import requests
import json
from config_data.config import RAPID_API_KEY


def find_city(city_name: str) -> list:
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city_name, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    response = requests.get(url=url, headers=headers, params=querystring)
    data = json.loads(response.text)

    cities = list()
    city_id = list()
    for names in data['sr']:
        cities.append(names['regionNames']['fullName'])
        city_id.append(names['essId']['sourceId'])

    return list(zip(cities, city_id))


def get_hotel_name_list(city_id: str, check_in_day: int, check_in_month: int, check_in_year: int,
             check_out_day: int, check_out_month: int, check_out_year: int) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": check_in_day,
            "month": check_in_month,
            "year": check_in_year
        },
        "checkOutDate": {
            "day": check_out_day,
            "month": check_out_month,
            "year": check_out_year
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {
            "max": 10000,
            "min": 100
        }}
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    hotel_names = list()
    hotel_id = list()
    for values in data['data']['propertySearch']['properties']:
        hotel_names.append(values['name'])
        hotel_id.append(values['id'])
    return list(zip(hotel_names, hotel_id))


def get_hotel_photos(hotel_id: str, photos_quantity: int) -> list[str]:
    """Находим фотографии по id отелей и возвращаем ссылки на img"""
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    image_list: list[str] = list()

    for images in data['data']['propertyInfo']['propertyGallery']['images'][0:photos_quantity]:
        image_list.append(images['image']['url'])
    return image_list
