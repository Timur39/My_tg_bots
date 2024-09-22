import random
import telebot
import requests
import time
from telebot import types
from telebot.types import ReplyKeyboardMarkup

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'
bot = telebot.TeleBot(token)

name = 'Капибара'
pet_image = ''
energy = 70
satiety = 30
happiness = 80


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.InlineKeyboardButton('Кот')
    item2 = types.InlineKeyboardButton('Собака')
    item3 = types.InlineKeyboardButton('Капибара')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, f'Выбери своего питомца', reply_markup=markup)
    bot.register_next_step_handler(message, second_step_start_handler)


def second_step_start_handler(message):
    global pet_image, name
    name_pet = message.text.lower()
    if name_pet == 'кот':
        pet_image = 'https://favim.com/pd/p/orig/2018/08/05/drawing-kitten-animals-Favim.com-6146459.jpg'
    elif name_pet == 'собака':
        pet_image = 'https://creazilla-store.fra1.digitaloceanspaces.com/cliparts/70736/puppy-clipart-md.png'
    elif name_pet == 'капибара':
        pet_image = 'https://i.pinimg.com/736x/fb/64/ba/fb64ba983f81f6cd2bb0d5ea9c4029c1.jpg'
    else:
        bot.send_message(message.chat.id, 'Такого питомца не существует!')
        return
    name = name_pet.capitalize()
    hideBoard = types.ReplyKeyboardRemove()
    bot.send_photo(message.chat.id, photo=pet_image, caption=f'Вы выбрали питомца: {name_pet}!', reply_markup=hideBoard)


def feed(food):
    global satiety, energy
    if food == 'яблоко':
        satiety += 10 if satiety < 100 else 0
        energy += 10 if energy < 100 else 0
    elif food == 'бутерброд':
        satiety += 15 if satiety < 100 else 0
        energy += 5 if energy < 100 else 0
    elif food == 'шоколадка':
        satiety += 5 if satiety < 100 else 0
        energy += 15 if energy < 100 else 0


def play(game):
    global happiness, energy, satiety
    if game == 'камень ножницы бумага':
        happiness += 20 if happiness < 100 else 0
        energy -= 15 if energy >= 0 else 0
        satiety -= 10 if happiness >= 0 else 0


def sleep():
    global energy, satiety, happiness
    energy = 70
    satiety -= 5 if satiety >= 0 else 0
    happiness -= 5 if happiness >= 0 else 0


def rock_scissors_paper(user_answer, computer_answer):
    if user_answer == computer_answer:
        return 'сыграл в ничью'
    elif user_answer == 'бумага' and computer_answer == 'камень':
        return 'победил'
    elif user_answer == 'камень' and computer_answer == 'ножницы':
        return 'победил'
    elif user_answer == 'ножницы' and computer_answer == 'бумага':
        return 'победил'
    else:
        return 'проиграл'


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_photo(message.chat.id, photo=pet_image, caption=f'{name}\nУровень сытости: {satiety}\nУровень энергии: {energy}\nУровень счастья: {happiness}')


@bot.message_handler(commands=['feed'])
def feed_handler(message):
    foods = ['яблоко', 'бутерброд', 'шоколадка']
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton(foods[0])
    item2 = types.KeyboardButton(foods[1])
    item3 = types.KeyboardButton(foods[2])
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Каким ты продуктом хочешь накормить питомца?', reply_markup=markup)
    bot.register_next_step_handler(message, second_step_feed_handler, foods)


def second_step_feed_handler(message, foods):
    food = message.text
    text = check()
    if food in foods:
        feed(food)
        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, f'{name} съел(а): {food}\n{text}', reply_markup=hideBoard)
    else:
        bot.send_message(message.chat.id, 'Извините, но я не знаю такого продукта')


@bot.message_handler(commands=['sleep'])
def sleep_handler(message):
    sleep()
    text = check()
    bot.send_message(message.chat.id, f'{name} поспал(а)\n{text}')


@bot.message_handler(commands=['play'])
def play_handler(message):
    games = ['камень ножницы бумага']
    markup = types.ReplyKeyboardMarkup(row_width=3)
    item1 = types.KeyboardButton(games[0])
    markup.add(item1)
    bot.send_message(message.chat.id, f'В какую игру ты хочешь поиграть?', reply_markup=markup)
    bot.register_next_step_handler(message, second_step_play_handler, games)


def second_step_play_handler(message, games):
    game = message.text
    if game in games:
        play(game)
        hideBoard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, f'Ты выбрал игру: {game}\nВведи: камень, ножницы, бумага', reply_markup=hideBoard)
        bot.register_next_step_handler(message, third_step_play_handler)
    else:
        bot.send_message(message.chat.id, 'Извините, но я не знаю такой игры')


counter = 0


def third_step_play_handler(message):
    global counter
    user_answer = message.text.lower()
    for_game = ['камень', 'ножницы', 'бумага']
    computer_answer = random.choice(for_game)
    res = rock_scissors_paper(user_answer, computer_answer)
    if user_answer in for_game:
        if res == 'победил':
            counter += 1
        bot.send_message(message.chat.id, f'Компьютер выбрал: {computer_answer}\nТы {res}\nВведи: камень, ножницы, бумага')
        bot.register_next_step_handler(message, fourth_step_play_handler, for_game)
    else:
        bot.send_message(message.chat.id, 'Извините, но я не понимаю такого варианта ответа')


def fourth_step_play_handler(message, for_game):
    global counter
    user_answer = message.text.lower()
    computer_answer = random.choice(for_game)
    res = rock_scissors_paper(user_answer, computer_answer)
    if user_answer in for_game:
        if res == 'победил':
            counter += 1
        bot.send_message(message.chat.id, f'Компьютер выбрал: {computer_answer}\nТы {res}\nВведи: камень, ножницы, бумага')
        bot.register_next_step_handler(message, fifth_step_play_handler, for_game)
    else:
        bot.send_message(message.chat.id, 'Извините, но я не понимаю такого варианта ответа')


def fifth_step_play_handler(message, for_game):
    global counter
    user_answer = message.text.lower()
    computer_answer = random.choice(for_game)
    res = rock_scissors_paper(user_answer, computer_answer)
    text = check()
    if user_answer in for_game:
        if res == 'победил':
            counter += 1
        bot.send_message(message.chat.id, f'Компьютер выбрал: {computer_answer}\nТы {res}\nТы сыграл со счетом {counter}:{3 - counter}\n\n{text}')
    else:
        bot.send_message(message.chat.id, 'Извините, но я не понимаю такого варианта ответа')


def check():
    res = []
    if satiety <= 0:
        res.append(f'{name} умер от голода')
    elif satiety <= 50:
        res.append(f'{name} хочет кушать!')
    elif satiety >= 50:
        res.append(f'{name} наелся и счастлив!')
    if happiness <= 0:
        res.append(f'{name} умер от тоски. С питомцем надо чаще играть')
    elif happiness <= 50:
        res.append(f'{name} хочет играть!')
    elif happiness >= 50:
        res.append(f'{name} счастлив как никогда!')
    if energy <= 0:
        res.append(f'{name} умер от истощения')
    elif energy <= 50:
        res.append(f'{name} хочет спать!')
    elif energy >= 50:
        res.append(f'{name} полон сил и энергии!')
    return '\n'.join(res)


@bot.message_handler()
def text_handler(message):
    bot.send_message(message.chat.id, 'Вы ввели неправильное значение. Попробуйте /start /info /feed /sleep /play')


bot.polling(none_stop=True)
