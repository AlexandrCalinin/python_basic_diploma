from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def commands():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = KeyboardButton(text='/lowprice')
    btn2 = KeyboardButton(text='/highprice')
    btn3 = KeyboardButton(text='/bestdeal')
    btn4 = KeyboardButton(text='/history')
    markup.add(btn1, btn2, btn3, btn4)
    return markup
