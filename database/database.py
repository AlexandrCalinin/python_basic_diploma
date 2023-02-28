from peewee import *
from loguru import logger
from datetime import datetime


db = SqliteDatabase('database/db.db')


class BaseModel(Model):
    """Класс базовой модели для ORM"""

    class Meta:
        database: SqliteDatabase = db
        order_by = 'id'


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

    class Meta:
        db_table = 'user'


class HotelsSearch(BaseModel):
    """
    Класс для хранения общей информации об отеле

    Attributes:
        command - команда
        user - объект класса User
        city - название города
        city_id - id города
        date_time - дата и время поиска
        date_in - дата въезда
        date_out - дата выезда
        hotels_amount - количество отелей
        photos_amount - количество фотографий
        min_price - минимальная цена
        max_price - максимальная цена
    """

    command = CharField(),
    user = Field(),
    city = CharField(),
    city_id = IntegerField(),
    date_time = DateField(),
    date_in = DateField(),
    date_out = DateField(),
    hotels_amount = IntegerField(),
    photos_amount = IntegerField(),
    min_price = IntegerField(),
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
    hotels_search = Field()
    name = CharField()
    address = CharField()
    price = IntegerField()
    distance = IntegerField()

    class Meta:
        db_table = 'hotels'


class Photo(BaseModel):
    """
    Класс фотографий для их сохранения

    Attributes:
        hotel - объект класса Hotel
        url - ссылки на фотографии
    """

    hotel = Field()
    url = CharField()

    class Meta:
        db_table = 'photos'


@logger.catch
def create_tables():
    """Создает таблицы в базе данных, если они не созданы"""
    with db:
        if not db:
            db.create_tables([User, HotelsSearch, Hotel, Photo])


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
            date_time=datetime.strptime(data['date_time'], '%d.%m.%Y %H:%M:%S'),
            date_in=datetime.strptime(data['arrival_date'], '%d.%m.%Y'),
            date_out=datetime.strptime(data['departure_date'], '%d.%m.%Y'),
            hotels_amount=int(data['hotels_quantity']),
            photos_amount=int(data['hotel_photo_quantity']),
            min_price=int(data['min_price']),
            max_price=int(data['max_price'])
        )

        for i_hotel in data['hotels']:
            hotel = Hotel.create(
                hotels_search=hotels_search,
                name=i_hotel['hotel'],
                hotel_id=int(i_hotel['hotel_id']),
                address=i_hotel['address'],
                distance=int(i_hotel['distance']),
                price=int(i_hotel['price'])
            )
            for photo in i_hotel['photos_list']:
                Photo.create(hotel=hotel, url=photo)
