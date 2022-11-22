from states.__init__ import MyStates
from loader import bot


@bot.message_handler(commands=['lowprice'])
def lowprice():
    print(MyStates())
