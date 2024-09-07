import random

import requests
import telebot
from telebot import types

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'

bot = telebot.TeleBot(token)

with open('cats.txt', 'r', encoding='utf-8') as file:
    cats = file.readlines()

with open('dogs.txt', 'r', encoding='utf-8') as file:
    dogs = file.readlines()
with open('kapibara.txt', 'r', encoding='utf-8') as file:
    kapibara = file.readlines()


cat1 = open(file='Cats/веселый_кот.jpg', mode='rb')
cat2 = open(file='Cats/довольный_кот.jpg', mode='rb')
cat3 = open(file='Cats/забавный кот.jpg', mode='rb')
cat4 = open(file='Cats/кот_в_ужасе.jpg', mode='rb')
cat5 = open(file='Cats/крейзи_кот.jpg', mode='rb')
cat6 = open(file='Cats/поддерживающий_кот.jpg', mode='rb')
cat7 = open(file='Cats/поникший_кот.jpg', mode='rb')
cat8 = open(file='Cats/расстроенный_кот.jpg', mode='rb')
cat9 = open(file='Cats/удивленный_кот.jpg', mode='rb')


@bot.message_handler(commands=['info_animals'])
def button(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton("Коты", callback_data='cats_id')
    item2 = types.InlineKeyboardButton("Собаки", callback_data='dogs_id')
    item3 = types.InlineKeyboardButton("Капибары", callback_data='kapibara_id')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Выберите животное:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    fact = ''
    if call.data == 'cats_id':
        fact = random.choice(cats)
    elif call.data == 'dogs_id':
        fact = random.choice(dogs)
    elif call.data == 'kapibara_id':
        fact = random.choice(kapibara)
    bot.send_message(call.message.chat.id, fact)


@bot.message_handler(commands=['cats_img'])
def button(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton('Весёлый кот')
    item2 = types.InlineKeyboardButton('Довольный кот')
    item3 = types.InlineKeyboardButton('Забавный кот')
    item4 = types.InlineKeyboardButton('Кот в ужасе')
    item5 = types.InlineKeyboardButton('Крейзи кот')
    item6 = types.InlineKeyboardButton('Поддерживающий кот')
    item7 = types.InlineKeyboardButton('Поникший кот')
    item8 = types.InlineKeyboardButton('Расстроенный кот')
    item9 = types.InlineKeyboardButton('Удивленный кот')
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    bot.send_message(message.chat.id, 'Выберите картинку кота:', reply_markup=markup)


@bot.message_handler()
def answer(message):
    if message.text == 'Весёлый кот':
        bot.send_photo(message.chat.id, cat1)
    if message.text == 'Довольный кот':
        bot.send_photo(message.chat.id, cat2)
    if message.text == 'Забавный кот':
        bot.send_photo(message.chat.id, cat3)
    if message.text == 'Кот в ужасе':
        bot.send_photo(message.chat.id, cat4)
    if message.text == 'Крейзи кот':
        bot.send_photo(message.chat.id, cat5)
    if message.text == 'Поддерживающий кот':
        bot.send_photo(message.chat.id, cat6)
    if message.text == 'Поникший кот':
        bot.send_photo(message.chat.id, cat7)
    if message.text == 'Расстроенный кот':
        bot.send_photo(message.chat.id, cat8)
    if message.text == 'Удивленный кот':
        bot.send_photo(message.chat.id, cat9)


bot.polling(none_stop=True)
