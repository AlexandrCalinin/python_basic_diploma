import requests
import json
from config_data.config import RAPID_API_KEY


def find_city(city_name: str) -> dict:
    """
    Функция поиска возможных вариантов локаций
    :param city_name: Название города для API запроса;
    :return: Словарь {точное название: id}
    """
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city_name, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
    response = requests.get(url=url, headers=headers, params=querystring)
    data = json.loads(response.text)

    locations_dict = dict()
    for names in data['sr'][0:5]:
        locations_dict[str(names['regionNames']['fullName'])] = names['essId']['sourceId']

    return locations_dict


def get_hotel_name_list(city_id: str, check_in_day: int, check_in_month: int, check_in_year: int,
                        check_out_day: int, check_out_month: int,
                        check_out_year: int, hotel_quantity: int) -> tuple[dict, list, list]:
    """
    Функция поиска названий отелей и их Id
    :param hotel_quantity: Нужное количество отелей
    :param city_id: Id города
    :param check_in_day: День въезда
    :param check_in_month: Месяц въезда
    :param check_in_year: Год въезда
    :param check_out_day: День выезда
    :param check_out_month: Месяц выезда
    :param check_out_year: Год выезда
    :return: Список [название отеля, его Id]
    """
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
    hotel_dict = dict()
    price = list()
    distance_from_center = list()
    for values in data['data']['propertySearch']['properties'][0:hotel_quantity]:
        hotel_dict[values['name']] = values['id']
        price.append(round(values['price']['lead']['amount'], 2))
        distance_from_center.append(round(values['destinationInfo']['distanceFromDestination']['value'] * 1.609, 2))
    return hotel_dict, price, distance_from_center


def structure_hotel_info(hotel_name: str, hotel_id: str, photos_quantity: int,
                         price: int, distance_from_center: int) -> dict:
    """
    Функция, структурирующая информацию об отеле
    :param distance_from_center: Дистанция в километрах от центра
    :param price: Цена за одну ночь
    :param photos_quantity: Нужное количество фотографий отеля
    :param hotel_id: Id отеля
    :param hotel_name: Название отеля
    :return: Структурированная информация об отеле
    """
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

    hotel_info = {
        'name': hotel_name,
        'id': hotel_id,
        'url': f'https://www.hotels.com/h{hotel_id}.Hotel-Information',
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'price': price,
        'distance': distance_from_center,
        'latitude': [latitude['mapMarker']['latLong']['latitude']
                     for latitude in data['data']['propertyInfo']['summary']['map']['markers'][:1]],
        'longitude': [longitude['mapMarker']['latLong']['longitude']
                     for longitude in data['data']['propertyInfo']['summary']['map']['markers'][:1]],
        'photo': [images['image']['url']
                  for images in data['data']['propertyInfo']['propertyGallery']['images'][0:photos_quantity]]
    }
    return hotel_info
