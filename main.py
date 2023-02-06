import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    logger.add('bot.log', format='{time} {level} {message}', level='DEBUG', rotation='10KB', compression='zip')
    logger.info('Бот вышел в онлайн...')
    set_default_commands(bot)
    bot.infinity_polling()
