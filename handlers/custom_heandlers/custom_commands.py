from telebot.types import InputMediaPhoto
from datetime import date
from states.state import MyStates
from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline import keyboard_for_city, keyboard_for_photos
from request_api import requests
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loguru import logger
from database.database import data_for_db


@logger.catch
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def command(message: Message):
    """
    Начинаем работать с командами, запрашиваем название города
    :param message: Объект Message
    """
    try:
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.set_state(message.from_user.id, MyStates.command, message.chat.id)
        logger.info(f'Пользователь {message.from_user.id} ввел команду {command.__name__}')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['command'] = str(message.text)[1:]
            data['user_id'] = str(message.from_user.id)
            data['user_name'] = str(message.from_user.first_name)
            if data['command'] == 'lowprice':
                data['sort'] = "PRICE_LOW_TO_HIGH"
                bot.send_message(message.chat.id, 'Здравствуйте! Это функция поиска отелей по низким ценам. '
                                                  'Укажите город для поиска: ')
            elif data['command'] == 'highprice':
                data['sort'] = "PRICE_HIGH_TO_LOW"
                bot.send_message(message.chat.id, 'Здравствуйте! Это функция поиска отелей по высоким ценам. '
                                                  'Укажите город для поиска: ')
            elif data['command'] == 'bestdeal':
                data['sort'] = "DISTANCE"
                bot.send_message(message.chat.id, 'Здравствуйте! Это функция поиска отелей с наилучшим предложением по '
                                                  'заданным критериям. Укажите город для поиска: ')
    except Exception as exc:
        print(exc)


@logger.catch
@bot.message_handler(state=MyStates.command)
def get_city(message: Message) -> None:
    """
    Запрашиваем у пользователя город, к котором нужно искать отели
    :param message: Объект Message
    """
    try:
        logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_city.__name__}')
        if message.text.isalpha():
            bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city'] = str(message.text)
            bot.send_message(message.chat.id, 'Я нашел несколько вариантов, выберите подходящий: ',
                             reply_markup=keyboard_for_city.keyboard(city_name=str(message.text), message=message))
        else:
            raise TypeError
    except TypeError:
            bot.send_message(message.chat.id, 'Название города должно содержать только буквы! Попробуйте еще раз.')
            get_city(message=message)


@logger.catch
@bot.callback_query_handler(func=lambda call: True, state=MyStates.city)
def callback_city(call: CallbackQuery):
    """
    Получаем ответ пользователя, путем нажатия на inline-кнопки, записываем город и его Id
    :param call: Объект CallbackQuery
    """
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {callback_city.__name__}')

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data['city_id'] = str(call.data)
        if data['command'] == 'bestdeal':
            bot.set_state(call.from_user.id, MyStates.price, call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Введите цену за ночь в долларах (через тире)')
        else:
            bot.set_state(call.from_user.id, MyStates.city_id, call.message.chat.id)
            bot.send_message(call.message.chat.id, 'Укажите количество отелей, которое необходимо '
                                                   'вывести в результате (максимум 10): ')


@logger.catch
@bot.message_handler(state=MyStates.price)
def get_price(message: Message) -> None:
    """
    При выборе команды bestdeal запрашиваем минимальную и максимальную цену за ночь
    :param message: Объект Message
    """
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_price.__name__}')
    bot.set_state(message.from_user.id, MyStates.city_id, message.chat.id)

    price = str(message.text).split('-')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['min_price'] = int(price[0])
        data['max_price'] = int(price[1])
    bot.send_message(message.chat.id, 'Укажите количество отелей, которое необходимо '
                                           'вывести в результате (максимум 10): ')


@logger.catch
@bot.message_handler(state=MyStates.city_id)
def to_send_photos(message: Message) -> None:
    """
    Путем inline клавиатуры спрашиваем у пользователя надобность клавиатуры
    :param message: Объект Message
    """
    try:
        logger.info(f'Пользователь {message.from_user.id} перешел в функцию {to_send_photos.__name__}')
        if message.text.isdigit() and 0 < int(message.text) < 11:
            bot.set_state(message.from_user.id, MyStates.number_of_hotels, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotels_quantity'] = str(message.text)
            bot.send_message(message.chat.id, 'Хотите вывести фотографии?', reply_markup=keyboard_for_photos.keyboard())
        else:
            raise TypeError
    except TypeError or ValueError:
            bot.send_message(message.chat.id, 'Ошибка! Одно из условий нарушено. Попробуйте еще раз!')
            to_send_photos(message=message)


@logger.catch
@bot.callback_query_handler(func=lambda call: True, state=MyStates.number_of_hotels)
def callback_get_photos_quantity(call: CallbackQuery) -> None:
    """
    Запрашиваем у пользователя количество фотографий отелей, которое нужно найти
    :param call: Объект CallbackQuery
    """
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
            data['hotel_photo_quantity'] = 0
        calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
        bot.send_message(call.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@bot.message_handler(state=MyStates.send_photos)
def get_arrival_date(message: Message) -> None:
    """
    Используя модуль календаря устанавливаем дату въезда
    :param message: Объект Message
    """
    logger.info(f'Пользователь {message.from_user.id} перешел в функцию {get_arrival_date.__name__}')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        bot.set_state(message.from_user.id, MyStates.number_of_hotel_photos, message.chat.id)
        data['hotel_photo_quantity'] = int(message.text)
    calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
    bot.send_message(message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)


@logger.catch
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def callback_arrival_date(call: CallbackQuery):
    """
    С помощью inline клавиатуры устанавливаем дату заезда
    :param call: Объект CallbackQuery
    """
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
            bot.set_state(call.from_user.id, MyStates.checkin_day, call.message.chat.id)
            bot.edit_message_text(f"Выбранная дата заезда: {result.strftime('%d-%m-%Y')}",
                                  call.message.chat.id,
                                  call.message.message_id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['arrival_date'] = result.strftime('%d-%m-%Y')
            calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
            bot.send_message(call.message.chat.id, f"Select {LSTEP[step]}", reply_markup=calendar)
    except Exception as exc:
        print(exc)


@logger.catch
@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def callback_departure_date(call: CallbackQuery):
    """
    С помощью inline клавиатуры устанавливаем дату выезда
    :param call: Объект CallbackQuery
    """
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
            bot.edit_message_text(f"Выбранная дата выезда: {result.strftime('%d-%m-%Y')}",
                                  call.message.chat.id,
                                  call.message.message_id)
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['departure_date'] = result.strftime('%d-%m-%Y')
            withdraw_hotels(call=call)
    except Exception as exc:
        print(exc)


@logger.catch
def withdraw_hotels(call) -> None:
    """
    Выводим заданное кол-во отелей и фотографии с их описанием
    """
    logger.info(f'Пользователь {call.from_user.id} перешел в функцию {withdraw_hotels.__name__}')
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        city_id = data['city_id']
        arrival_date = data['arrival_date']
        check_in_date = arrival_date.split('-')
        departure_date = data['departure_date']
        check_out_date = departure_date.split('-')
        hotel_dict, price, distance = requests.get_hotel_name_list(city_id=str(city_id),
                                                                   check_in_day=int(check_in_date[0]),
                                                                   check_in_month=int(check_in_date[1]),
                                                                   check_in_year=int(check_in_date[2]),
                                                                   check_out_day=int(check_out_date[0]),
                                                                   check_out_month=int(check_out_date[1]),
                                                                   check_out_year=int(check_out_date[2]),
                                                                   hotel_quantity=int(data['hotels_quantity']),
                                                                   sort=data['sort'],
                                                                   min_price=data['min_price']
                                                                   if data['command'] == 'bestdeal' else None,
                                                                   max_price=data['max_price']
                                                                   if data['command'] == 'bestdeal' else None)

        counter = 0
        for hotel_names, hotel_id in hotel_dict.items():
            request = requests.structure_hotel_info(hotel_name=hotel_names, hotel_id=hotel_id,
                                                    photos_quantity=data['hotel_photo_quantity'],
                                                    price=price[counter], distance_from_center=distance[counter])
            if data['hotel_photo_quantity'] > 0:
                media = [InputMediaPhoto(request['photo'][indexes], caption=f"Название отеля: {request['name']}\n"
                                         f"Адрес отеля: {request['address']}\n"
                                         f"Цена за ночь: {request['price']} долларов (2 взрослых, 2 ребенка)\n"
                                         f"Расстояние от центра: {request['distance']} км")
                         if len(request['photo']) - indexes == 1 else InputMediaPhoto(request['photo'][indexes])
                          for indexes in range(0, len(request['photo']))]
                bot.send_media_group(call.message.chat.id, media)
            else:
                bot.send_message(call.message.chat.id, f"Название отеля: {request['name']}\n"
                                                       f"Адрес отеля: {request['address']}\n"
                                                       f"Цена за ночь: {request['price']} "
                                                       f"долларов (1 взрослый, 2 ребенка)\n"
                                                       f"Расстояние от центра: {request['distance']} км")
            data['hotel_id'] = str(hotel_id)
            data_for_db(data=data)
            counter += 1
