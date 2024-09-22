import datetime
import telebot

token = '7338743074:AAFi9DWQH8Fj2nzZjeyG4RgmKpHACN3e_ls'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['birthday'])
def birthday(message):
    bot.send_message(message.chat.id, '¬ведите дату вашего рождени€ в формате год-мес€ц-день')


@bot.message_handler()
def get_birthday(message):
    temp = message.text.split('-')
    temp = list(map(lambda x: int(x), temp))
    current_day = datetime.datetime.now()
    birthday1 = datetime.datetime(current_day.year, temp[1], temp[2])
    birthday2 = datetime.datetime(current_day.year + 1, temp[1], temp[2])
    result = (birthday1 if birthday1 > current_day else birthday2) - current_day
    bot.send_message(message.chat.id, f'{result.days}')


bot.polling(none_stop=True)