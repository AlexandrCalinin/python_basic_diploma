from loader import bot
from loguru import logger
from database.database import *


@bot.message_handler(commands=['/history'])
def get_history():
    pass