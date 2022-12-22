from states.state import MyStates
from telebot.types import Message
from loader import bot
from keyboards.inline import keyboard_for_city


@bot.message_handler(commands=['lowprice'])
def get_city_name(message):
    """Запрашиваем у пользователя город, к котором нужно искать отели"""
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, 'Укажите город, в котором хотите найти отели.')
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = str(message.text)


@bot.message_handler(state=MyStates.city)
def concretize_the_city(message: Message) -> None:
    bot.send_message(message.chat.id, 'Я нашел несколько вариантов, выберите подходящий: ',
                     reply_markup=keyboard_for_city.keyboard(str(message.text)))
    bot.set_state(message.from_user.id, MyStates.concretize_city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['concretize_city'] = str(message.text)


@bot.message_handler(state=MyStates.concretize_city)
def get_number_of_hotels(message: Message) -> None:
    """Запрашиваем у пользователя количество отелей, которое нужно найти"""
    bot.send_message(message.chat.id, 'Укажите количество отелей, которое необходимо вывести в результате: ')
    bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotels_quantity'] = int(message.text)


@bot.message_handler(state=MyStates.number_of_hotels, is_digit=True)
def get_number_of_hotel_photos(message: Message) -> None:
    """Запрашиваем у пользователя количество фотографий отелей, которое нужно найти"""
    bot.send_message(message.chat.id, 'Хотите вывести фотографии? (Да/Нет).')

    if message.text.title() == 'Да':
        bot.set_state(MyStates.send_photos, True)
        bot.send_message(message.chat.id, 'Введите количество необходимых фотографий.')
        bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['send_photos'] = True
            data['hotel_photo_quantity'] = int(message.text)

    elif message.text.title() == 'Нет':
        MyStates.send_photos = False
        bot.set_state(message.from_user.id, MyStates.send_photos, message.chat.id)
        MyStates.number_of_hotel_photos = 0
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['send_photos'] = MyStates.send_photos
            data['hotel_photo_quantity'] = MyStates.number_of_hotel_photos

    else:
        bot.send_message(message.chat.id, 'Такого варианта ответа нет. Попробуйте еще раз!')


@bot.message_handler(state=[MyStates.city, MyStates.number_of_hotels,
                            MyStates.send_photos, MyStates.number_of_hotel_photos], is_digit=True)
def print_result(message: Message) -> None:
    """Выводим результат состояний"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Готово, взгляните:\n<b>"
               f"Город: {data['concretize_city']}\n"
               f"Количество отелей: {data['hotels_quantity']}\n"
               f"Количество фотографий: {data['hotels_quantity']}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
