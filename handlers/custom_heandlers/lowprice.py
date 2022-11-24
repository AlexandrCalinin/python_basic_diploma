from states import state
from loader import bot


@bot.message_handler(commands=['lowprice'])
def lowprice(message):
    bot.send_message(message.chat.id, 'Привет! Эта функция низких цен.')
    print(state.MyStates())
