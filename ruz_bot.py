import requests
import json
import telebot
import multilangual as ml
from telebot import types
from config import token
from user import User, get_str_for_user
from database_of_users import DatabaseOfUsers


d = DatabaseOfUsers('databases/database.json')
bot = telebot.TeleBot(token)


def search_id(term, type):
    url = f"https://ruz.hse.ru/api/search?term={term}&type={type}"
    response = requests.get(url)
    data = response.json()
    return data

@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
    user = User(str(message.from_user.id), ml.select_language_or_default(message.from_user.language_code))
    d.add_new_user(user)
    d.dump()
    bot.send_message(message.chat.id, get_str_for_user(user, 'Hello'))


@bot.message_handler(func=lambda message: d.get_user_information_by_id(str(message.from_user.id)).stage == 0)
def search_message(message: types.Message):
    data = search_id(message.text.strip(), 'student')
    if len(data) == 0:
        bot.send_message(message.chat.id, get_str_for_user(d[message.from_user.id], "No results"))
    elif len(data) >= 7:
        bot.send_message(message.chat.id, get_str_for_user(d[message.from_user.id], "A lot results"))
    else:
        answer = ''
        for i, student in enumerate(data, 1):
            answer += f'{i}. {student["label"]}\n\t{student["description"]}\n\n'
        bot.send_message(message.chat.id, answer)


if __name__ == '__main__':
    ml.load_language_packs()
    bot.infinity_polling()
