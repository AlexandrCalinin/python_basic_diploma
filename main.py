import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger
from database.database import *


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    logger.add('bot.log', format='{time} {level} {message}', level='DEBUG')
    logger.info('Бот вышел в онлайн...')
    set_default_commands(bot)
    bot.infinity_polling()
