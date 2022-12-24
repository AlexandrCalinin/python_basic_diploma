from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from request_api import requests


def keyboard(city_name):
    list_of_cities = requests.find_city(city_name)
    tuple_of_names, tuple_of_id = zip(*list_of_cities)

    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text=tuple_of_names[0], callback_data='btn1')
    btn2 = InlineKeyboardButton(text=tuple_of_names[1], callback_data='btn2')
    btn3 = InlineKeyboardButton(text=tuple_of_names[2], callback_data='btn3')
    btn4 = InlineKeyboardButton(text=tuple_of_names[3], callback_data='btn4')
    btn5 = InlineKeyboardButton(text=tuple_of_names[4], callback_data='btn5')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup
