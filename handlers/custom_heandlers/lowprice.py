from request_api import requests
from telebot.types import Message
from loader import bot
from telebot.handler_backends import State, StatesGroup


class CommandStates(StatesGroup):
    city: str = State()
    concretize_city: str = State()
    number_of_hotels: int = State()
    send_photos: bool = State()
    number_of_hotel_photos: int = State()


@bot.message_handler(commands=['lowprice'])
def command(message: Message) -> None:
    """ Ловим команду lowprice и устанавливаем первое состояние city """
    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.set_state(message.from_user.id, CommandStates.city, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, укажите город '
                                               f'для поиска самых дешевых отелей', parse_mode='Markdown')
    except Exception as exc:
        print(exc)
    finally:
        print(CommandStates.city)


@bot.message_handler(state=CommandStates.city)
def get_city(message: Message) -> None:
    """
    Здесь ловим ответ пользователя, проверяем на корректность,
    устанавливаем второе состояние с помощью inline-клавиатуры
    """
    print(CommandStates.city)