import random

import requests
import telebot
from telebot import types

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'

bot = telebot.TeleBot(token)

res = 0
count = 0


@bot.message_handler(commands=['test'])
def button(message):
    global count
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with open('questions.txt', 'r', encoding='utf-8') as file:
        questions = [i.replace('\n', '') for i in file.readlines()]
    with open('answers.txt', 'r', encoding='utf-8') as file:
        answers = [i.replace('\n', '') for i in file.readlines()]

    if count < len(questions):
        question = questions[count]
        item1 = types.KeyboardButton(answers[questions.index(question)].split('-')[0])
        item2 = types.KeyboardButton(answers[questions.index(question)].split('-')[1])
        if random.randint(0, 1) == 0:
            item1, item2 = item2, item1
        markup.add(item1, item2)
        bot.send_message(message.chat.id, question, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Тест окончен. Твой результат: {res} из {len(questions)}')


@bot.message_handler()
def answer(message):
    global res
    global count
    true_answer = 0
    with open('answers.txt', 'r', encoding='utf-8') as file:
        answers = [i.replace('\n', '') for i in file.readlines()]
    for i in range(len(answers)):
        if message.text in answers[i].split('-')[0]:
            res += 1
            true_answer += 1
            count += 1
            button(message)
            break
    if true_answer == 0:
        count += 1
        button(message)


bot.polling(none_stop=True)
