import random

import requests
import telebot

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'

bot = telebot.TeleBot(token)

poke_api_url = 'https://pokeapi.co/api/v2/pokemon/'


@bot.message_handler(commands=['pokemon'])
def send_random_poke_info(message):
    poke_id = random.randint(1, 898)
    url = poke_api_url + str(poke_id)
    response = requests.get(url)
    data = response.json()
    if 'sprites' in data and 'front_default' in data['sprites']:
        poke_name = data['name'].capitalize()
        poke_image_url = data['sprites']['front_default']
        poke_info = f'Имя: {poke_name}\nid: {poke_id}\nТип(ы): '
        for poke_type in data['types']:
            poke_info += f'{poke_type["type"]["name"]} '
        bot.send_photo(message.chat.id, photo=poke_image_url, caption=poke_info)


@bot.message_handler(commands=['all_pokemons'])
def send_all_pokemons(message):
    with open('file.txt', 'r', encoding='utf-8') as file:
        data = [i.replace('\n', '') for i in file.readlines()]
        res = []
        x = 0
        y = 7

        for i in range(0, len(data) // 7):
            for j in range(x, y):
                res += [data[j]]

            res_text = '\n'.join(res[0:5])
            bot.send_photo(message.chat.id, photo=res[5], caption=res_text)
            res = []
            x = y
            y += 7


@bot.message_handler()
def send_current_poke_info(message):
    url = poke_api_url + str(message.text.split(' ')[0].lower())
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'sprites' in data and 'front_default' in data['sprites']:
            poke_name = data['name'].capitalize()
            poke_id = data['id']
            poke_image_url = data['sprites']['front_default']
            poke_weight = data['weight']
            poke_height = data['height']
            poke_type = ', '.join([poke_type["type"]["name"] for poke_type in data['types']])
            poke_info = (f'Имя: {poke_name}\n'
                         f'id: {poke_id}\n'
                         f'Вес: {poke_weight}\n'
                         f'Рост: {poke_height}\n'
                         f'Тип(ы): {poke_type}\n')
            bot.send_photo(message.chat.id, photo=poke_image_url, caption=poke_info)

        if '+' in message.text:
            with open('file.txt', 'a', encoding='utf-8') as file:
                file.write(f'{poke_info}{poke_image_url}\n\n')
            bot.send_message(message.chat.id, f'Покемон {poke_name} успешно добавлен!')


bot.polling(none_stop=True)