from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from request_api import requests


def keyboard(city_name):
    list_of_cities = requests.find_city(city_name)
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text=list_of_cities[0], callback_data='btn1')
    btn2 = InlineKeyboardButton(text=list_of_cities[1], callback_data='btn2')
    btn3 = InlineKeyboardButton(text=list_of_cities[2], callback_data='btn3')
    btn4 = InlineKeyboardButton(text=list_of_cities[3], callback_data='btn4')
    btn5 = InlineKeyboardButton(text=list_of_cities[4], callback_data='btn5')
    return markup.add(btn1, btn2, btn3, btn4, btn5)
