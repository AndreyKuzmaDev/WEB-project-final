import asyncio
import vk_api
from dotenv import dotenv_values
from vk_api.longpoll import VkLongPoll, VkEventType
import random
from backend import recognize

TOKEN = dotenv_values('.env')['VK_TOKEN']

vk = vk_api.VkApi(token=TOKEN)
longpoll = VkLongPoll(vk)


def send_messages(chat_id, text):
    random_id = random.randint(0, 1000000)
    vk.method('messages.send', {'chat_id': chat_id, 'message': text, 'random_id': random_id})


async def real_timer(text, chat):
    data = text.split()
    time_int = int(data[1])
    time_type = 1
    if data[2] == 'M':
        time_type = 60
    elif data[2] == 'H':
        time_type = 3600
    await asyncio.sleep(time_int * time_type)
    random_id = random.randint(0, 1000000)
    vk.method('messages.send', {'chat_id': chat, 'message': 'Время вышло!', 'random_id': random_id})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.from_chat:
            msg = event.text
            chat_id = event.chat_id
            answer = recognize(msg)
            if answer.split()[0] == 'TIMER':
                send_messages(chat_id, 'Таймер установлен.')
                asyncio.run(real_timer(answer, chat_id))
            elif answer != 'NO_ANSWER':
                try:
                    send_messages(chat_id, answer)
                except Exception:
                    send_messages(chat_id, 'Слишком длинный ответ')


