import handlers
from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
from log_and_errors import logs


@logs.logger.catch
def main():
    bot.add_custom_filter(StateFilter(bot))
    print('Бот вышел в онлайн...')
    set_default_commands(bot)
    bot.infinity_polling()


if __name__ == '__main__':
    main()