from states.state import MyStates
from telebot.types import Message
from loader import bot
from keyboards.inline import keyboard_for_city, keyboard_for_photos
from request_api import requests


data1 = dict()


@bot.message_handler(commands=['lowprice'])
def command(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.set_state(message.from_user.id, MyStates.command, message.chat.id)
    bot.send_message(message.chat.id, 'Здравствуйте! Это функция поиска отелей по низким ценам. '
                                      'Укажите город для поиска: ')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = str(message.text)


@bot.message_handler(state=MyStates.command)
def get_city(message: Message) -> None:
    """Запрашиваем у пользователя город, к котором нужно искать отели"""
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = str(message.text)
        data1['city'] = str(message.text)
    bot.send_message(message.chat.id, 'Я нашел несколько вариантов, выберите подходящий: ',
                     reply_markup=keyboard_for_city.keyboard(str(message.text)))


@bot.callback_query_handler(func=lambda call: True, state=MyStates.city)
def callback(call):
    """ Получаем ответ пользователя, путем нажатия на inline-кнопки, записываем город и его id"""
    list_of_cities = requests.find_city(data1['city'])
    tuple_of_names, tuple_of_id = zip(*list_of_cities)

    if call.data == 'btn1':
        bot.send_message(call.message.chat.id, 'Вы выбрали 1 кнопку')
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[0])
        bot.set_state(MyStates.city_id, state=tuple_of_id[0])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[0]
            data['city_id'] = tuple_of_id[0]

    elif call.data == 'btn2':
        bot.send_message(call.message.chat.id, 'Вы выбрали 2 кнопку')
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[1])
        bot.set_state(MyStates.city_id, state=tuple_of_id[1])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[1]
            data['city_id'] = tuple_of_id[1]

    elif call.data == 'btn3':
        bot.send_message(call.message.chat.id, 'Вы выбрали 3 кнопку')
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[2])
        bot.set_state(MyStates.city_id, state=tuple_of_id[2])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[2]
            data['city_id'] = tuple_of_id[2]

    elif call.data == 'btn4':
        bot.send_message(call.message.chat.id, 'Вы выбрали 4 кнопку')
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[3])
        bot.set_state(MyStates.city_id, state=tuple_of_id[3])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[3]
            data['city_id'] = tuple_of_id[3]

    elif call.data == 'btn5':
        bot.send_message(call.message.chat.id, 'Вы выбрали 5 кнопку')
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[4])
        bot.set_state(MyStates.city_id, state=tuple_of_id[4])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[4]
            data['city_id'] = tuple_of_id[4]

    bot.send_message(call.message.chat.id, 'Укажите количество отелей, которое необходимо вывести в результате: ')


@bot.message_handler(state=MyStates.city)
def get_number_of_hotels(message: Message) -> None:
    """Запрашиваем у пользователя количество отелей, которое нужно найти"""
    bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['hotels_quantity'] = int(message.text)
    bot.send_message(message.chat.id, 'Хотите вывести фотографии? (Да/Нет).',
                     reply_markup=keyboard_for_photos.keyboard())


@bot.callback_query_handler(func=lambda call: True, state=MyStates.number_of_hotels)
def callback(call) -> None:
    """Запрашиваем у пользователя количество фотографий отелей, которое нужно найти"""

    if call.data == 'yes':
        bot.set_state(MyStates.send_photos, state='Да')
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['send_photos'] = 'Да'
        bot.send_message(call.message.chat.id, 'Введите количество необходимых фотографий: ')

    elif call.data == 'no':
        bot.set_state(MyStates.send_photos, state='Нет')
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['send_photos'] = 'Нет'


@bot.message_handler(state=MyStates.send_photos)
def to_send_photos(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        if MyStates.send_photos == 'Да':
            bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
            data['hotel_photo_quantity'] = int(message.text)

        if MyStates.send_photos == 'Нет':
            bot.set_state(MyStates.number_of_hotel_photos, state=0)
            data['hotel_photo_quantity'] = 0


@bot.message_handler(state=[MyStates.city, MyStates.number_of_hotels,
                            MyStates.send_photos, MyStates.number_of_hotel_photos])
def print_result(message: Message) -> None:
    """Выводим результат состояний"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Готово, взгляните:\n<b>"
               f"Город: {data['city']}\n"
               f"Точное местоположение: {data['concretize_city']}\n"
               f"Id города: {data['city_id']}\n"
               f"Количество отелей: {data['hotels_quantity']}\n"
               f"Количество фотографий: {data['hotels_quantity']}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
