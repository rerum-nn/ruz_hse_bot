import telebot
import multilangual as ml
from telebot import types
from config import token
from user import User, get_str_for_user
from database_of_users import DatabaseOfUsers
from search import Search

numbers_emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']

search = Search()
d = DatabaseOfUsers('databases/database.json')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
    user = User(str(message.from_user.id), ml.select_language_or_default(message.from_user.language_code))
    d.add_new_user(user)
    d.dump()
    bot.send_message(message.chat.id, get_str_for_user(user, 'Hello'))


@bot.message_handler(func=lambda message: d.get_user_information_by_id(str(message.from_user.id)).stage == 0)
def search_message(message: types.Message):
    search.search_id(message.text.strip(), 'student')
    if search.size == 0:
        bot.send_message(message.chat.id, get_str_for_user(d[message.from_user.id], "No results"))
    elif search.size >= 7:
        bot.send_message(message.chat.id, get_str_for_user(d[message.from_user.id], "A lot results"))
    elif search.size == 1:
        d[message.from_user.id].ruz_id = search.data[0]['id']
        d.dump()
        bot.send_message(message.from_user.id, f"{get_str_for_user(d[message.from_user.id], 'Student found')}:"
                                               f"\n\n{search.data[0]['label']}\n{search.data[0]['description']}")
    else:
        answer = f'{get_str_for_user(d[message.from_user.id], "Choice student")}:\n\n'
        keyboard = types.InlineKeyboardMarkup()
        buttons = []
        for i, student in enumerate(search.data, 1):
            answer += f'{i}. {student["label"]}\n       {student["description"]}\n\n'
            buttons.append(types.InlineKeyboardButton(numbers_emoji[i], callback_data=i))
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, answer, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: d[call.from_user.id].stage == 0)
def choice_student_callback(call: types.CallbackQuery):
    choice = int(call.data) - 1
    d[call.from_user.id].ruz_id = search.data[choice]['id']
    d.dump()
    bot.send_message(call.message.chat.id, f'{get_str_for_user(d[call.from_user.id], "Successfully choice")}:\n\n'
                                           f'{search.data[choice]["label"]}\n'
                                           f'       {search.data[choice]["description"]}')


if __name__ == '__main__':
    ml.load_language_packs()
    bot.infinity_polling()
