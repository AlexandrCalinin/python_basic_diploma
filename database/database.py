from peewee import *
from loguru import logger
from datetime import datetime


db = SqliteDatabase('users.db')

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
        chat_id - id чата
    """
    name = CharField()
    user_id = IntegerField(unique=True)
    chat_id = IntegerField()
    command = CharField()
    date = DateField()

    class Meta:
        db_table = 'user'


class City(BaseModel):
    """
    Класс для хранения информации о городе

    Attributes:
        user_id - id пользователя
        city - название города
        city_id - id города для поиска отелей
    """

    user_id = IntegerField(unique=True)
    city = IntegerField()
    city_id = IntegerField()

    class Meta:
        db_table = 'city'


class Hotels(BaseModel):
    """
    Класс для хранения информации об отеле

    Attributes:
        user_id - id пользователя
        hotel_id - id чата
        hotel_quantity - количество отелей
        hotel_photo_quantity - количество фотографий отеля
    """

    user_id = IntegerField(unique=True)
    hotel_id = IntegerField()
    hotel_quantity = IntegerField()
    hotel_photo_quantity = IntegerField()

    class Meta:
        db_table = 'hotels'


class Photos(BaseModel):
    """
    Класс фотографий для их сохранения

    Attributes:
        user_id - имя пользователя
        hotel_id - id отеля
        photos - ссылки на фотографии
    """

    user_id = IntegerField(unique=True)
    hotel_id = IntegerField(unique=True)
    photos = CharField()

    class Meta:
        db_table = 'photos'


@logger.catch
def create_tables():
    """Создает таблицы в базе данных, если они не созданы"""
    with db:
        if not db:
            db.create_tables([User, Hotels, Photos])


def data_for_db(data: dict) -> None:
    """
    Записывает данные в бд

    :param data: словарь с данными
    """

    with db.atomic():
        user = User.get_or_create(
            name = data['user_name'],
            user_id = data['user_id'],
            chat_id = data['chat_id'],
            command = data['command'],
            date = datetime.now()
        )

        city = City.get_or_create(
            user_id = data['user_id'],
            city = data['city'],
            city_id = data['city_id']
        )

        hotels = Hotels.get_or_create(
            user_id = data['user_id'],
            hotel_id = data['hotel_id'],
            hotel_quantity = data['hotels_quantity'],
            hotel_photo_quantity = data['hotel_photo_quantity']
        )

        photos = Photos.get_or_create(
            user_id = data['user_id'],
            hotel_id = data['hotel_id'],
            photos = data['urls']
        )