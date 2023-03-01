import os
from typing import List, Optional

from peewee import *
from datetime import datetime


db = SqliteDatabase(os.path.join('database', 'bot_data.db'))


class BaseModel(Model):
    """Класс базовой модели для ORM"""

    class Meta:
        database: SqliteDatabase = db


class User(BaseModel):
    """
    Класс пользователя для ORM

    Attributes:
        name - имя пользователя
        user_id - id пользователя
        command - выбранная команда
    """
    name = CharField()
    chat_id = IntegerField()
    user_id = IntegerField(unique=True)


class HotelsSearch(BaseModel):
    """
    Класс для хранения общей информации об отеле

    Attributes:
        command - команда
        user - объект класса User
        city - название города
        city_id - id города
        date_in - дата въезда
        date_out - дата выезда
        hotels_amount - количество отелей
        photos_amount - количество фотографий
        min_price - минимальная цена
        max_price - максимальная цена
    """

    command = CharField()
    user = ForeignKeyField(User, backref='Searches')
    city = CharField()
    city_id = IntegerField()
    date_time = DateTimeField()
    date_in = DateField()
    date_out = DateField()
    hotels_amount = IntegerField()
    photos_amount = IntegerField()
    min_price = IntegerField()
    max_price = IntegerField()


class Hotel(BaseModel):
    """
    Класс для хранения информации об отеле

    Attributes:
        hotel_id - id чата
        hotels_search - объект класса HotelsSearch
        name - название отеля
        address - адрес отеля
        price - цена за ночь
        distance - расстояние до центра
    """

    hotel_id = IntegerField()
    hotels_search = ForeignKeyField(HotelsSearch, backref='hotels')
    name = CharField()
    address = CharField()
    price = FloatField()
    distance = FloatField()


class Photo(BaseModel):
    """
    Класс фотографий для их сохранения

    Attributes:
        hotel - объект класса Hotel
        url - ссылки на фотографии
    """

    photos = ForeignKeyField(Hotel, backref='photos')
    url = CharField()


def data_for_db(data: dict) -> None:
    """
    Записывает данные в бд

    :param data: словарь с данными
    """

    with db.atomic():
        user = User.get_or_create(
            name=data['user_name'],
            user_id=int(data['user_id']),
            chat_id=int(data['chat_id'])
        )[0]

        hotels_search = HotelsSearch.create(
            command=data['command'],
            user=user,
            city=data['city'],
            city_id=int(data['city_id']),
            date_time=datetime.strptime(str(datetime.now().replace(microsecond=0, tzinfo=None)), '%Y-%m-%d %H:%M:%S'),
            date_in=datetime.strptime(data['arrival_date'], '%d-%m-%Y'),
            date_out=datetime.strptime(data['departure_date'], '%d-%m-%Y'),
            hotels_amount=int(data['hotels_quantity']),
            photos_amount=int(data['hotel_photo_quantity']),
            min_price=int(data['min_price']),
            max_price=int(data['max_price'])
        )

        hotel = Hotel.create(
            hotels_search=hotels_search,
            name=data['hotels']['name'],
            hotel_id=int(data['hotels']['id']),
            address=data['hotels']['address'],
            distance=int(data['hotels']['distance']),
            price=int(data['hotels']['price'])
        )
        for photo in data['hotels']['photo']:
            Photo.create(hotel=hotel, url=photo)


def hotels_searches_from_db(user_id: int) -> List[HotelsSearch]:
    """
    Извлекает из базы данных историю поисков отелей

    :param user_id: id пользователя
    :return: история поисков отелей
    """

    with db.atomic():
        query = HotelsSearch.select().join(User).where(User.user_id == user_id)
    query: list = list(query)

    return query


def hotel_photos_from_db(hotel: Hotel) -> List[Optional[str]]:
    """
    Извлекает из базы данных фотографии для отеля

    :param hotel: отель
    :return: список со ссылками на фотографии
    """

    photos_list = list()
    with db.atomic():
        if hotel.hotels_search.photos_amount:
            photos_list = [
                photo.url
                for photo in
                Photo.select().where(Photo.hotel == hotel)
            ]

    return photos_list


def hotels_data_from_db(hotels_search: HotelsSearch) -> list:
    """
    Извлекает из базы данных данные по отелям для поиска отелей из истории поиска

    :param hotels_search: поиск отелей
    :return: список с данными по отелям
    """

    with db.atomic():
        query = Hotel.select().where(Hotel.hotels_search == hotels_search)

    hotels = list()
    for hotel in query:
        hotels.append({
            'hotel': hotel.name,
            'hotel_id': hotel.hotel_id,
            'address': hotel.address,
            'distance': hotel.distance,
            'price': hotel.price,
            'photos_list': hotel_photos_from_db(hotel)
        })

    return hotels
