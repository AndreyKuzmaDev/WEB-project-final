from backend import recognize
from dotenv import dotenv_values
import telebot
import asyncio

bot = telebot.TeleBot(dotenv_values('.env')['TG_TOKEN'])


@bot.message_handler(content_types=['text'])
def text_commands(message):
    response = recognize(message.text)
    if response.split()[0] == 'TIMER':
        bot.send_message(message.chat.id, 'Таймер установлен.')
        asyncio.run(real_timer(response, message.chat.id))
    else:
        bot.send_message(message.chat.id, response)


async def real_timer(text, chat):
    data = text.split()
    time_int = int(data[1])
    time_type = 1
    if data[2] == 'M':
        time_type = 60
    elif data[2] == 'H':
        time_type = 3600
    await asyncio.sleep(time_int * time_type)
    bot.send_message(chat, 'Время вышло!')

bot.polling(non_stop=True)
