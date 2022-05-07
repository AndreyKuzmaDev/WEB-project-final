from sympy.solvers import solve
from bs4 import BeautifulSoup
from requests import request
from random import choice, randint
from sympy import Symbol
import datetime
import json


# Функция, распознающая команды пользователя по ключевым словам
def recognize(text):
    data = json.load(open('data.json', 'rb'))
    data['messages'].append(text)
    with open('data.json', 'w') as output:
        json.dump(data, output, indent=4)
    if text.split()[0].lower() == 'бот':
        text = text.lower()
        for i in KEY_WORDS.keys():
            if i in text:
                return KEY_WORDS[i](text)
        return 'Не понял команду, попробуйте ещё раз.'
    return 'NO_ANSWER'


def random_message(stat):
    messages = json.load(open('data.json', 'rb'))['messages']
    max_len = 0
    for i in messages:
        if len(i.split()) > max_len:
            max_len = len(i.split())
    length = randint(1, max_len)
    generated = []
    while len(generated) < length:
        msg = choice(messages).split()
        if len(msg) > len(generated):
            generated.append(msg[len(generated)])
    return ' '.join(generated)


# Последняя новость
def news(text):
    url = 'https://yandex.ru/news?msid=1645874415555541-10935585541354775902-sas5' \
          '-9946-38a-sas-l7-balancer-8080-BAL-8146&mlid=1645873938.glob_225&utm_source' \
          '=morda_desktop&utm_medium=topnews_news'
    html = request(method='GET', url=url).content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return '\n\n'.join(list(map(lambda x: x.text,
                                soup.find_all('div', class_='mg-card__annotation')))[:5:])


# Сообщить время
def time(*args):
    return str(datetime.datetime.now().time()).split('.')[0]


# Сообщить дату
def date(*args):
    return str(datetime.datetime.now().date()).split('.')[0]


# Случайное число
def random_int(text, *args):
    data = text.split()
    begin = 1
    end = 2 ** 16
    for i in range(len(data)):
        if data[i] == 'от':
            begin = int(data[i + 1])
        elif data[i] == 'до':
            end = int(data[i + 1])
    return str(choice(range(begin, end + 1)))


# Повторение сообщения
def repeat(text, *args):
    return f'Я получил сообщение "{text}".'


# Вызов таймера в боте
def fake_timer(text, *args):
    try:
        data = text.split()
        response = 'TIMER ' + str(data[data.index('на') + 1])
        if 'минут' in text:
            response += ' M'
        elif 'час' in text:
            response += ' H'
        else:
            response += ' S'
        return response
    except Exception:
        return 'Не понял команду, попробуйте ещё раз.'


# Случайная шутка на заданную тему из data.json
def joke(text, *args):
    jokes = json.load(open('data.json', 'rb'))['jokes']
    for i in THEMES.keys():
        if i in text:
            return choice(jokes[THEMES[i]])
    return 'Выберите тему: программисты, армия, Штирлиц'


# Решение уравнения
def equation(text):
    try:
        eq = text.split(':')[1]
        if '/0' in eq:
            raise ZeroDivisionError
        x = Symbol('x')
        eq = f"{eq.split('=')[0]} - ({eq.split('=')[1]})"
        res = list(map(str, list(solve(eq.lower(), x))))
        if len(res) == 0:
            return 'Нет решений'
        res = '\n'.join(res)
        return res
    except IndexError:
        return 'Поставьте перед уравнением двоеточие'
    except ZeroDivisionError:
        return 'На ноль делить нельзя'
    except Exception:
        return 'Введите корректное уравнение'


# Решение примера
def problem(text):
    try:
        pr = text.split(':')[1]
        res = str(eval(pr))
        return res
    except IndexError:
        return 'Поставьте перед примером двоеточие'
    except ZeroDivisionError:
        return 'На ноль делить нельзя'


def write_pi(text):
    try:
        data = text.split()
        pi = open('pi.txt').read()
        s = 'знаков'
        for i in data:
            if 'знак' in i:
                s = i
                break
        n = int(data[data.index(s) - 1])
        if n >= 4000:
            raise IndexError
        res = pi[:n + 2]
        return res
    except IndexError:
        return 'Максимум знаков после запятой - 4000'
    except Exception:
        return 'Напишите сколько знаков должно быть после запятой'


# Ключевые слова
KEY_WORDS = {'новости': news,
             'рандомное число': random_int,
             'случайное число': random_int,
             'назови число': random_int,
             'повтори': repeat,
             'врем': time,
             'дата': date,
             'дату': date,
             'сегодняшнее число': date,
             'пошути': joke,
             'анекдот': joke,
             'шутк': joke,
             'таймер': fake_timer,
             'уравне': equation,
             'пример': problem,
             'вычисли': problem,
             'сгенерируй': random_message,
             'число пи': write_pi}


# Темы для шуток
THEMES = {'программист': 'programmers',
          'штирлиц': 'stirlitz',
          'арм': 'army'}
