import requests
import telebot
import multilangual as ml
import datetime as dt
from datetime import date, datetime
from telebot import types
from config import token
from user import User, get_str_for_user
from database_of_users import DatabaseOfUsers
from search import Search

numbers_emoji = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']

menu_keyboard = types.ReplyKeyboardMarkup()
search = Search()
d = DatabaseOfUsers('databases/database.json')
bot = telebot.TeleBot(token)

modes_of_print = ["Weekly schedule", "Daily schedule"]


def init_keyboard_settings(user: User):
    main_button1 = types.KeyboardButton(get_str_for_user(user, "Change a student"))
    main_button2 = types.KeyboardButton(get_str_for_user(user, "Change the display mode"))
    menu_keyboard.add(main_button1)
    menu_keyboard.add(main_button2)
    menu_keyboard.resize_keyboard = True
    menu_keyboard.one_time_keyboard = True


@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
    user = User(str(message.from_user.id), message.from_user.language_code)
    d.add_new_user(user)
    d.dump()
    init_keyboard_settings(user)
    bot.send_message(message.chat.id, get_str_for_user(user, 'Hello'), reply_markup=types.ReplyKeyboardRemove())


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
        d[message.from_user.id].stage = 1
        bot.send_message(message.from_user.id, f"{get_str_for_user(d[message.from_user.id], 'Student found')}:"
                                               f"\n\n{search.data[0]['label']}\n{search.data[0]['description']}")
        choice_the_mode_of_print(d[message.from_user.id])
        d.dump()
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
    d[call.from_user.id].stage = 1
    bot.send_message(call.message.chat.id, f'{get_str_for_user(d[call.from_user.id], "Successfully choice")}:\n\n'
                                           f'{search.data[choice]["label"]}\n'
                                           f'       {search.data[choice]["description"]}')
    choice_the_mode_of_print(d[call.from_user.id])
    d.dump()


def choice_the_mode_of_print(user: User):
    if user.mode == 0:
        show_week_schedule_for_user(user)
    elif user.mode == 1:
        show_everyday_schedule_for_user(user)


def show_everyday_schedule_for_user(user: User):
    day = (datetime.today() + dt.timedelta(hours=3)).date()

    if not show_schedule_on_day(user, day, menu_keyboard):
        bot.send_message(user.telegram_id, get_str_for_user(user, "No classes"), reply_markup=menu_keyboard)


def show_week_schedule_for_user(user: User):
    week_begin = date.today() + dt.timedelta(days=1)
    week_begin = week_begin - dt.timedelta(days=week_begin.weekday())

    lessons_on_week = False

    for week_day in [week_begin + dt.timedelta(days=i) for i in range(7)]:
        lessons_on_week = show_schedule_on_day(user, week_day, menu_keyboard) or lessons_on_week

    if not lessons_on_week:
        bot.send_message(user.telegram_id, get_str_for_user(user, "No classes on week"), reply_markup=menu_keyboard)


def show_schedule_on_day(user: User, dt_: date, keyboard = types.ReplyKeyboardRemove()):
    response = requests.get(f'https://ruz.hse.ru/api/schedule/student/{user.ruz_id}'
                           f'?start={dt_.strftime("%Y.%m.%d")}'
                           f'&finish={dt_.strftime("%Y.%m.%d")}'
                           f'&lng={"1" if user.language == "ru" else "2"}').json()

    answer = get_str_for_user(user, f'{dt_.weekday()}_week') + f' ({dt_.strftime("%d.%m.%Y")}):\n\n'

    for lecture in response:
        answer += f'*({lecture["beginLesson"]}-{lecture["endLesson"]}) {lecture["discipline"]}* \n' \
            f'({lecture["kindOfWork"]}) \n' \
            f'_{lecture["auditorium"]} ({lecture["building"]})_\n' \
            f'{lecture["lecturer"]}\n'
        if lecture['note']:
            answer += f'_{lecture["note"]}_\n'
        if lecture['url1']:
            answer += f'{lecture["url1"]}\n'
        answer += '\n\n'

    if len(response) != 0:
        bot.send_message(user.telegram_id, answer, disable_web_page_preview=True, parse_mode="Markdown",
                         reply_markup=keyboard)
        return True
    elif user.get_show_empty_day(dt_.weekday()):
        answer += get_str_for_user(user, "No classes")
        bot.send_message(user.telegram_id, answer, disable_web_page_preview=True, parse_mode="Markdown",
                         reply_markup=keyboard)
    else:
        return False


@bot.message_handler(func=lambda message: message.text == get_str_for_user(d[message.from_user.id], "Change a student"))
def change_student(message: types.Message):
    d[message.from_user.id].stage = 0
    bot.send_message(message.from_user.id, get_str_for_user(d[message.from_user.id], "Enter the student's name"),
                     reply_markup=types.ReplyKeyboardRemove())
    d.dump()


@bot.message_handler(func=lambda message: message.text == get_str_for_user(d[message.from_user.id],
                                                                           "Change the display mode"))
def change_print_mode(message: types.Message):
    d[message.from_user.id].stage = 2
    inline_keyboard = types.InlineKeyboardMarkup()
    for c, i in enumerate(modes_of_print, 0):
        inline_keyboard.add(types.InlineKeyboardButton(get_str_for_user(d[message.from_user.id], i),
                                                       callback_data=str(c)))
    bot.send_message(message.from_user.id, get_str_for_user(d[message.from_user.id], "Select the display mode"),
                     reply_markup=inline_keyboard)
    d.dump()


@bot.callback_query_handler(func=lambda call: d[call.from_user.id].stage == 2)
def change_print_mode_callback(call: types.CallbackQuery):
    d[call.from_user.id].mode = int(call.data)
    d[call.from_user.id].stage = 1
    d.dump()
    choice_the_mode_of_print(d[call.from_user.id])


if __name__ == '__main__':
    ml.load_language_packs()
    bot.infinity_polling()
