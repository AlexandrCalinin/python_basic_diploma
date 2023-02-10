from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from request_api import requests
from loader import bot
from telebot.types import Message


def keyboard(city_name: str, message: Message) -> InlineKeyboardMarkup | None:
    """
    Клавиатура с вариантами локаций
    :param city_name: Название города, в котором нудно искать конкретные локации
    :param message: Объект Message
    :return: Если найдены локации, то клавиатура с приближенными локациями, в противном случае None
    """
    locations_dict = requests.find_city(city_name)
    markup = InlineKeyboardMarkup(row_width=1)

    if locations_dict:
        for concrete_location, city_id in locations_dict.items():
            markup.add(InlineKeyboardButton(text=concrete_location, callback_data=city_id))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['locations_dict'] = locations_dict
        return markup
    return None
