from telebot.types import Message
from keyboards.reply import keyboard_for_commands

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.full_name}! "
                                           f"Выбери команду из списка, чтобы начать работу.",
                     reply_markup=keyboard_for_commands.commands())
