from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    command = State()
    city = State()
    concretize_city = State()
    city_id = State()
    number_of_hotels = State()
    send_photos = State()
    number_of_hotel_photos = State()
    arrival_date = State()
    checkin_day = State()
    departure_date = State()
    checkout_day = State()