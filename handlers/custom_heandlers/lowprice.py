from states import state
from telebot.types import Message
from loader import bot
from telebot.handler_backends import State, StatesGroup


@bot.message_handler(commands=['lowprice'])
def command(message: Message) -> None:
    """ Ловим команду lowprice и подключаем состояния """