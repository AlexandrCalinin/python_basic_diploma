import telebot


bot = telebot.TeleBot('5945288735:AAEvoJOeWfyzj1C9F8Z8VVLlxTn9kdrpWpY')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start' or message.text == '/hello-world':
        bot.send_message(message.from_user.id, "Рад пиветствовать Вас в нашем телеграмм боте по поиску отелей!")
    elif message.text.title() == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
