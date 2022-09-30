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
    user = User(message.from_user.id, ml.select_language_or_default(message.from_user.language_code))
    d.add_new_user(user)
    d.dump()
    bot.send_message(message.chat.id, get_str_for_user(user, 'Hello'))


if __name__ == '__main__':
    ml.load_language_packs()
    bot.infinity_polling()
