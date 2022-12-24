from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    command: str = State()
    city: str = State()
    concretize_city: str = State()
    city_id: str = State()
    number_of_hotels: int = State()
    send_photos: str = State()
    number_of_hotel_photos: int = State()
