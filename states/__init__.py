from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
from loader import bot


state_storage = StateMemoryStorage()


class MyStates(StatesGroup):
    city: str = State()
    number_of_hotels: int = State()
    send_photos: bool = State()
    number_of_hotel_photos: int = State()


@bot.message_handler(state=MyStates.city)
def get_city_name(message):
    """Запрашиваем у пользователя город, к котором нужно искать отели"""
    bot.send_message(message.chat.id, 'Укажите город, в котором хотите найти отели')
    MyStates.city = str(message.text)
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = MyStates.city


@bot.message_handler(state=MyStates.number_of_hotels, is_digit=True)
def get_number_of_hotels(message):
    """Запрашиваем у пользователя количество отелей, которое нужно найти"""
    bot.send_message(message.chat.id, 'Укажите количество отелей, которые необходимо вывести в результате')

    if isinstance(message.text, int):
        MyStates.number_of_hotels = message.text
    else:
        bot.send_message(message.chat.id,'Введите числоб пожалуйтса!')

    bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotels_quantity'] = MyStates.number_of_hotels


@bot.message_handler(state=[MyStates.send_photos, MyStates.number_of_hotel_photos], is_digit=True)
def get_number_of_hotel_photos(message):
    """Запрашиваем у пользователя количество фотографий отелей, которое нужно найти"""
    bot.send_message(message.chat.id, 'Хотите вывести фотографии? (Да/Нет)')

    if message.text.title() == 'Да':
        MyStates.send_photos = True
        bot.set_state(message.from_user.id, MyStates.send_photos, message.chat.id)
        bot.send_message(message.chat.id, 'Введите количество необходимых фотографий')
        MyStates.number_of_hotel_photos = int(message.text)
        bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['send_photos'] = MyStates.send_photos
            data['hotel_photo_quantity'] = MyStates.number_of_hotel_photos

    elif message.text.title() == 'Нет':
        MyStates.send_photos = False
        bot.set_state(message.from_user.id, MyStates.send_photos, message.chat.id)
        MyStates.number_of_hotel_photos = 0
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['send_photos'] = MyStates.send_photos
            data['hotel_photo_quantity'] = MyStates.number_of_hotel_photos

    else:
        bot.send_message(message.chat.id, 'Такого варианта ответа нет. Попробуйте еще раз')


@bot.message_handler(state=[MyStates.city, MyStates.number_of_hotels,
                             MyStates.send_photos, MyStates.number_of_hotel_photos], is_digit=True)
def print_result(message):
    """Выводим результат состояний"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Готово, взгляните:\n<b>"
               f"Город: {data['city']}\n"
               f"Количество отелей: {data['hotels_quantity']}\n"
               f"Количество фотографий: {data['hotels_quantity']}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
