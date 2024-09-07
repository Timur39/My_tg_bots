import random
import requests
import telebot

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'

bot = telebot.TeleBot(token)

poke_api_url = 'https://pokeapi.co/api/v2/pokemon/'


@bot.message_handler()
def send_current_poke_info(message):
    url = poke_api_url + str(message.text.lower())
    response = requests.get(url)
    data = response.json()

    if 'sprites' in data and 'front_default' in data['sprites']:
        poke_name = data['name'].capitalize()
        poke_id = data['id']
        poke_image_url = data['sprites']['front_default']
        poke_weight = data['weight']
        poke_height = data['height']
        poke_base_experience = data['base_experience']
        poke_info = f'Имя: {poke_name}\nid: {poke_id}\nВес: {poke_weight}\nРост: {poke_height}\nБазовый опыт: {poke_base_experience}\nТип(ы): '

        for poke_type in data['types']:
            poke_info += f'{poke_type["type"]["name"]} '
        bot.send_photo(message.chat.id, photo=poke_image_url, caption=poke_info)


bot.polling(none_stop=True)
