from telebot.types import Message

from loader import bot
from loguru import logger
from database.database import *


@logger.catch
@bot.message_handler(commands=['/history'])
def get_history(message: Message):
    """
    Вывод истории поиска
    :param message - Объект класса Message
    """
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_history.__name__}')