from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def keyboard():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Да', callback_data='Да')
    btn2 = InlineKeyboardButton(text='Нет', callback_data='Нет')
    markup.add(btn1, btn2)
    return markup
