# Бот для любых социальных сетей

# Авторы
Павел Провоторов и Андрей Кузьма

# Описание
Программа имеет две части:
Бэкэнд и сам бот

Наша реализация бэкэнда работает при помощи функции recognize, которая принимает в себя текст сообщения и с помощью ключевых слов определяет что хотел пользователь и на осове этого генерирует текстовый ответ или команду для бота

Сам бот принимая сообщение просто передает его в бэкэнд и либо отправляет ответ, либо выполняет переданные команды (например поставить таймер)

Благодаря такой реализации нашего бота можно практически моментально перенести в любую другую социальную сеть или мессенджер

# Использование бота

Чтобы воспользоваться нашим ботом необходимо запустить файл для нужного вам приложения (Telegram, VK, Discord)

В файле .env содержатся токены для аккаунтов которые мы создали для ботов. Если вы хотите запустить нашего бота на другом аккаунте вам нужно только изменить токены в этом файле

# Реализованные возможности бота

Чтобы бот выполнил команду напишите сообщение которое начинается со слова "бот"

Наш бот может:

Отправлять последние новости

Сообщать время и дату

Ставить таймер

Случайно выбирать число в заданном диапазоне

Повторять полученное сообщение

Решать примеры и уравнения

Рассаказывать анекдоты на заданную тему

Генерировать сообщения на основе других сообщений в беседе

# Планируемые возможности бота

Записывать статистику по пользователям

Находить информацию в Google 


