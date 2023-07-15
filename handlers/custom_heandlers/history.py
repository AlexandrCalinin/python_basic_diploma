from telebot.types import Message

from loader import bot
from loguru import logger
from database.database import *


@logger.catch
@bot.message_handler(commands=['history'])
def get_history(message: Message):
    """
    Вывод истории поиска
    :param message - Объект класса Message
    """
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_history.__name__}')
    hotels_search_result = hotels_searches_from_db(int(message.from_user.id))

    for hotels in hotels_search_result:
        data = hotels_data_from_db(hotels)
        bot.send_message(message.chat.id, f"Команда: {data[0]['command']}\n"
                                          f"Дата поиска: {data[0]['creation_date']}\n"
                                          f"Название отеля: {data[0]['hotel']}\n"
                                          f"Адрес отеля: {data[0]['address']}\n"
                                          f"Расстояние до центра: {data[0]['distance']}\n"
                                          f"Цена за ночь: {data[0]['price']} долларов")
