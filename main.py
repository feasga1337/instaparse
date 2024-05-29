import random
import time

from instagrapi import Client
import telebot
from telebot import types
from userclass import User


token = ''

ACCOUNT_USERNAME = ''
ACCOUNT_PASSWORD = ''

cl = Client()
cl.delay_range = [7, 15]

cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)


bot = telebot.TeleBot(token, parse_mode=None)
users = {}


@bot.message_handler(commands=['start', 'help', "Меню", "menu", "Menu", "Start", 'Help'])
def SendWelcome(message):
    if message.chat.id != 479845437:
        msg = ''
        if message.chat.username is not None:
            msg = f'{msg}  @{message.chat.username} :'
        if message.chat.first_name is not None:
            msg = f'{msg} {message.chat.first_name} :'
        if message.chat.last_name is not None:
            msg = f"{msg} {message.chat.last_name}"
        bot.send_message(479845437, text=f"{msg}", reply_markup=None)
    try:
        users[message.chat.id].user_menu = 'menu'


    except:
        users[message.chat.id] = User()
        users[message.chat.id].user_menu = 'menu'

    global feedback_btn, checkUnFollow_btn

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    checkUnFollow_btn = types.KeyboardButton("Посмотреть мудаков🤡")

    feedback_btn = types.KeyboardButton("Написать создателю(хочу свои пять копеек вставить)")

    markup.add(checkUnFollow_btn, feedback_btn)

    bot.send_message(message.chat.id, text=f'Нихао, {message.chat.first_name}! Чё ты хочешь от меня?',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def Buttons(message):
    if users[message.chat.id].user_menu == "menu":
        if message.text == feedback_btn.text:
            Feedback(message)
            users[message.chat.id].user_menu = "feedback"
        elif message.text == checkUnFollow_btn.text:
            CheckUnFollow(message)
            users[message.chat.id].user_menu = "checkunfollow"

    elif message.text == "Отминэт":
        SendWelcome(message)
    elif users[message.chat.id].user_menu == 'feedback':
        bot.send_message(479845437, text=f'{message.chat.id}:{message.chat.first_name}: {message.text}')
    elif users[message.chat.id].user_menu == "checkunfollow":
        try:
            followers_username = []
            following_username = []
            pidors = []
            user_id = cl.user_id_from_username(message.text)

            followers = cl.user_followers(user_id)

            time.sleep(5)
            following = cl.user_following(user_id)
            for x in followers:
                followers_username.append(followers[x].username)
            for x in following:
                following_username.append(following[x].username)
            for pidor in following_username:
                if pidor in followers_username:
                    continue
                else:
                    pidors.append(pidor)
            if len(pidors) > 0:
                bot.send_message(message.chat.id, text=f'Эти одноклеточные на тебя не подпсаны {pidors}')
                print(message.chat.first_name, pidors)
            else:
                bot.send_message(message.chat.id, text='Усё добра, твои подписчики, походу, умерли')
                print('ахуеть')
            SendWelcome(message)
        except:
            bot.send_message(message.chat.id, text='Или ты объебался, или санки не едут, или я де то накосячил. Я верю, что это ты мудень')
            SendWelcome(message)


@bot.message_handler()
def Feedback(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отминэт')
    markup.add(btn1)
    bot.send_message(message.chat.id, text='Ну калякай шо нибудь, а я мб отвечу', reply_markup=markup)


@bot.message_handler()
def CheckUnFollow(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Отминэт')
    markup.add(btn1)
    bot.send_message(message.chat.id, text='Инсту свою сюда черкани', reply_markup=markup)


bot.infinity_polling()
