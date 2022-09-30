import requests
import json
import telebot
from telebot import types
from config import token
from user import User

bot = telebot.TeleBot(token)


def search_id(term, type):
    url = f"https://ruz.hse.ru/api/search?term={term}&type={type}"
    response = requests.get(url)
    data = response.json()
    return data


@bot.message_handler(commands=['start'])
def start_message(message: types.Message):

    bot.send_message(message.chat.id, 'Привет👋, введи свои имя, чтобы бот смог найти твое расписание')

def print_results_of_search():



if __name__ == '__main__':
    bot.infinity_polling()
