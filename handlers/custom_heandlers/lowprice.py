from datetime import date
from states.state import MyStates
from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline import keyboard_for_city, keyboard_for_photos
from request_api import requests
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


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
    if message.text.isalpha():
        bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = str(message.text)
            data1['city'] = str(message.text)
        bot.send_message(message.chat.id, 'Я нашел несколько вариантов, выберите подходящий: ',
                         reply_markup=keyboard_for_city.keyboard(str(message.text)))
    else:
        bot.send_message(message.chat.id, 'Название города должно содержать только буквы! Попробуйте еще раз.')
        get_city(message=message)


@bot.callback_query_handler(func=lambda call: True, state=MyStates.city)
def callback_city(call: CallbackQuery):
    """ Получаем ответ пользователя, путем нажатия на inline-кнопки, записываем город и его id"""
    list_of_cities = requests.find_city(data1['city'])
    tuple_of_names, tuple_of_id = zip(*list_of_cities)

    if call.data == 'btn1':
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[0])
        bot.set_state(MyStates.city_id, state=tuple_of_id[0])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[0]
            data['city_id'] = tuple_of_id[0]

    elif call.data == 'btn2':
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[1])
        bot.set_state(MyStates.city_id, state=tuple_of_id[1])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[1]
            data['city_id'] = tuple_of_id[1]

    elif call.data == 'btn3':
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[2])
        bot.set_state(MyStates.city_id, state=tuple_of_id[2])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[2]
            data['city_id'] = tuple_of_id[2]

    elif call.data == 'btn4':
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[3])
        bot.set_state(MyStates.city_id, state=tuple_of_id[3])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[3]
            data['city_id'] = tuple_of_id[3]

    elif call.data == 'btn5':
        bot.set_state(MyStates.concretize_city, state=tuple_of_names[4])
        bot.set_state(MyStates.city_id, state=tuple_of_id[4])
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[4]
            data['city_id'] = tuple_of_id[4]

    bot.send_message(call.message.chat.id, 'Укажите количество отелей, которое необходимо '
                                           'вывести в результате (максимум 10): ')


@bot.message_handler(state=MyStates.city)
def to_send_photos(message: Message) -> None:
    """Спрашиваем нужны ли пользователю фотографии"""
    if message.text.isdigit() and int(message.text) < 11:
        bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_quantity'] = str(message.text)
        bot.send_message(message.chat.id, 'Хотите вывести фотографии?', reply_markup=keyboard_for_photos.keyboard())
    else:
        bot.send_message(message.chat.id, 'Ошибка! Одно из условий нарушено. Попробуйте еще раз!')
        to_send_photos(message=message)


@bot.callback_query_handler(func=lambda call: MyStates.number_of_hotel_photos)
def callback_get_photos_quantity(call: CallbackQuery) -> None:
    """Запрашиваем у пользователя количество фотографий отелей, которое нужно найти"""
    if call.data == 'Да':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.set_state(call.from_user.id, MyStates.send_photos, call.message.chat.id)
            data['send_photos'] = 'Да'
            bot.send_message(call.message.chat.id, 'Введите количество необходимых фотографий (максимум 10): ')
    elif call.data == 'Нет':
        calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
        bot.send_message(call.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@bot.message_handler(state=MyStates.send_photos)
def get_arrival_date(message: Message) -> None:
    """Используя модуль календаря устанавливаем дату въезда"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
        data['hotel_photo_quantity'] = str(message.text)
        calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
        bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_arrival_date(call: CallbackQuery):
    print(1)
    try:
        bot.set_state(call.from_user.id, MyStates.arrival_date, call.message.chat.id)
        result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru',
                                                     min_date=date.today()).process(call.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['arrival_date'] = str(result)
            bot.send_message(call.message.chat.id, f"Вы выбрали: {result}")
    except Exception as exc:
        print(exc)
    finally:
        calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
        bot.send_message(call.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_departure_date(call: CallbackQuery):
    try:
        bot.set_state(call.from_user.id, MyStates.departure_date, call.message.chat.id)
        result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru',
                                                     min_date=date.today()).process(call.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['departure_date'] = str(result)
            bot.send_message(call.message.chat.id, f"Вы выбрали: {result}")
    except Exception as exc:
        print(exc)


@bot.message_handler(state=MyStates.departure_date)
def withdraw_hotels(message: Message) -> None:
    """Выводим заданное кол-во отелей и фотографии с их описанием"""
    # bot.set_state(message.from_user.id, MyStates.departure_confirmation, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        city_id = data['city_id']
        arrival_date = data['arrival_date']
        check_in_date = arrival_date.split('-')
        departure_date = data['departure_date']
        check_out_date = departure_date.split('-')
        req_result = requests.get_hotel_name_list(city_id=str(city_id), check_in_day=int(check_in_date[2]),
                                                  check_in_month=int(check_in_date[1]),
                                                  check_in_year=int(check_in_date[0]),
                                                  check_out_day=int(check_out_date[2]),
                                                  check_out_month=int(check_out_date[1]),
                                                  check_out_year=int(check_out_date[0]))

        tuple_of_hotel_names, tuple_of_hotel_id = zip(*req_result)
        hotel_names = list()
        hotel_id = list()
        for indexes in range(1, int(data['hotels_quantity']) + 1):
            hotel_names.append(tuple_of_hotel_names[indexes])
            hotel_id.append(tuple_of_hotel_id[indexes])

        for index in range(1, int(data['hotels_quantity']) + 1):
            image_urls = requests.get_hotel_photos(hotel_id=hotel_id[index - 1],
                                                   photos_quantity=int(data['hotel_photo_quantity']))
            print(image_urls)
        print('Готово!')
