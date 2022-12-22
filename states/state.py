from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    city: str = State()
    concretize_city: str = State()
    number_of_hotels: int = State()
    send_photos: bool = State()
    number_of_hotel_photos: int = State()
