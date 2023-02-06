from datetime import date
from states.state import MyStates
from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline import keyboard_for_city, keyboard_for_photos
from request_api import requests
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loguru import logger

data1 = dict()


@logger.catch
@bot.message_handler(commands=['lowprice'])
def command(message):
    """Начинаем работать с lowprice, запрашиваем название города"""
    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.set_state(message.from_user.id, MyStates.command, message.chat.id)
        logger.info(f'Пользователь {message.from_user.id} ввел команду {command.__name__}')
        bot.send_message(message.chat.id, 'Здравствуйте! Это функция поиска отелей по низким ценам. '
                                          'Укажите город для поиска: ')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['command'] = str(message.text)
    except Exception as exc:
        print(exc)


@logger.catch
@bot.message_handler(state=MyStates.command)
def get_city(message: Message) -> None:
    """Запрашиваем у пользователя город, к котором нужно искать отели"""
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_city.__name__}')
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


@logger.catch
@bot.callback_query_handler(func=lambda call: True, state=MyStates.city)
def callback_city(call: CallbackQuery):
    """ Получаем ответ пользователя, путем нажатия на inline-кнопки, записываем город и его id"""
    list_of_cities = requests.find_city(data1['city'])
    tuple_of_names, tuple_of_id = zip(*list_of_cities)
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {callback_city.__name__}')

    if call.data == 'btn1':
        bot.set_state(call.from_user.id, MyStates.concretize_city, call.message.chat.id)
        bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[0]
            data['city_id'] = tuple_of_id[0]

    elif call.data == 'btn2':
        bot.set_state(call.from_user.id, MyStates.concretize_city, call.message.chat.id)
        bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[1]
            data['city_id'] = tuple_of_id[1]

    elif call.data == 'btn3':
        bot.set_state(call.from_user.id, MyStates.concretize_city, call.message.chat.id)
        bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[2]
            data['city_id'] = tuple_of_id[2]

    elif call.data == 'btn4':
        bot.set_state(call.from_user.id, MyStates.concretize_city, call.message.chat.id)
        bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[3]
            data['city_id'] = tuple_of_id[3]

    elif call.data == 'btn5':
        bot.set_state(call.from_user.id, MyStates.concretize_city, call.message.chat.id)
        bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['concretize_city'] = tuple_of_names[4]
            data['city_id'] = tuple_of_id[4]

    bot.send_message(call.message.chat.id, 'Укажите количество отелей, которое необходимо '
                                           'вывести в результате (максимум 10): ')


@logger.catch
@bot.message_handler(state=MyStates.city_id)
def to_send_photos(message: Message) -> None:
    """Спрашиваем нужны ли пользователю фотографии"""
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {to_send_photos.__name__}')
    if message.text.isdigit() and int(message.text) < 11:
        bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_quantity'] = str(message.text)
        bot.send_message(message.chat.id, 'Хотите вывести фотографии?', reply_markup=keyboard_for_photos.keyboard())
    else:
        bot.send_message(message.chat.id, 'Ошибка! Одно из условий нарушено. Попробуйте еще раз!')
        to_send_photos(message=message)


@logger.catch
@bot.callback_query_handler(func=lambda call: True, state=MyStates.number_of_hotels)
def callback_get_photos_quantity(call: CallbackQuery) -> None:
    """Запрашиваем у пользователя количество фотографий отелей, которое нужно найти"""
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {callback_get_photos_quantity.__name__}')
    if call.data == 'Да':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.set_state(call.from_user.id, MyStates.send_photos, call.message.chat.id)
            data['send_photos'] = 'Да'
            bot.send_message(call.message.chat.id, 'Введите количество необходимых фотографий (максимум 10): ')
    elif call.data == 'Нет':
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            bot.set_state(call.from_user.id, MyStates.send_photos, call.message.chat.id)
            data['send_photos'] = 'Да'
        calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
        bot.send_message(call.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@bot.message_handler(state=MyStates.send_photos)
def get_arrival_date(message: Message) -> None:
    """Используя модуль календаря устанавливаем дату въезда"""
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_arrival_date.__name__}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
        data['hotel_photo_quantity'] = str(message.text)
    calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_arrival_date(call: CallbackQuery):
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {callback_arrival_date.__name__}')
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
            bot.edit_message_text(f"Выбранная дата заезда: {result.strftime('%d-%m-%Y')}",
                                  call.message.chat.id,
                                  call.message.message_id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['arrival_date'] = result.strftime('%d-%m-%Y')
    except Exception as exc:
        print(exc)


@logger.catch
@bot.message_handler(state=MyStates.arrival_date)
def departure_day(message: Message) -> None:
    """Используя модуль календаря, устанавливаем дату выезда"""
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {departure_day.__name__}')
    bot.set_state(message.from_user.id, MyStates.checkin_day, message.chat.id)
    calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_departure_date(call: CallbackQuery):
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {callback_departure_date.__name__}')
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
            bot.set_state(call.from_user.id, MyStates.checkout_day, call.message.chat.id)
            bot.edit_message_text(f"Выбранная дата заезда: {result.strftime('%d-%m-%Y')}",
                                  call.message.chat.id,
                                  call.message.message_id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['departure_date'] = result.strftime('%d-%m-%Y')
    except Exception as exc:
        print(exc)


@logger.catch
@bot.message_handler(state=MyStates.checkout_day)
def withdraw_hotels(message: Message) -> None:
    """Выводим заданное кол-во отелей и фотографии с их описанием"""
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {withdraw_hotels.__name__}')
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
