import asyncio
import discord
from dotenv import dotenv_values

from backend import recognize

TOKEN = dotenv_values('.env')['DS_TOKEN']


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg = message.content
        answer = recognize(msg)
        if answer.split()[0] == 'TIMER':
            await message.channel.send('Таймер установлен.')
            asyncio.run(real_timer(answer, message.channel))
        else:
            await message.channel.send(answer)


async def real_timer(text, chat):
    data = text.split()
    time_int = int(data[1])
    time_type = 1
    if data[2] == 'M':
        time_type = 60
    elif data[2] == 'H':
        time_type = 3600
    await asyncio.sleep(time_int * time_type)
    chat.send('Время вышло!')


client = YLBotClient()
client.run(TOKEN)
