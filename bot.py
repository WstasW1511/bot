import telebot
import environs
import main
from main import *
from datetime import datetime
import os


env = environs.Env()
env.read_env(os.path.join('app.conf'))
bot = telebot.TeleBot(env.str('TOKEN'))


def log(message):
    print(" ------------")
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2})\nТекст - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop',)  # добавляем команды
    user_markup.row('Новости Tengrinews.kz')
    bot.send_message(message.from_user.id, 'Добро пожаловать', reply_markup=user_markup)
    log(message)

@bot.message_handler(commands=["stop"])
def handle_start(message):  # функция, которая убирает нашу клавиатуру
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, '...', reply_markup=hide_markup)
    log(message)

count = 0
count1 = 1
id_sms=[]
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global count
    global count1
    global id_sms
    if message.text == 'Новости Tengrinews.kz':
        id_sms.append(message.id)
        main.start(1)
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Загрузить 8 последних (текст)", 'Загрузить 5 последних ссылок')
        user_markup.row('Назад 8', 'Назад 5', 'Очистить')
        bot.send_message(message.from_user.id, 'Новости tengrinews.kz', reply_markup=user_markup)
        bot.send_message(message.from_user.id, "Всего " + str(len(news)) + " Новостей")
    if message.text == 'Загрузить 8 последних (текст)':
        id_sms.append(message.id)
        if count < len(news):
            for key in range(count, count+8):
                bot.send_message(message.from_user.id,news[key])
            count += 8
        else:
            bot.send_message(message.from_user.id, "Вы загрузили все новости")

    if message.text == 'Назад 8':
        id_sms.append(message.id)
        if count != 0:
            for key in range(count-8, count):
                bot.send_message(message.from_user.id, news[key])
            count -= 8
        else:
            bot.send_message(message.from_user.id, "Вы загрузили все новости")

    log(message)

    if message.text == 'Загрузить 5 последних ссылок':
        id_sms.append(message.id)
        if count1 < len(links):
            for key in range(count1, count1 + 5):
                bot.send_message(message.from_user.id, links[key])
            count1 += 5
        else:
            bot.send_message(message.from_user.id, "Вы загрузили все новости")
    if message.text == 'Назад 5':
        id_sms.append(message.id)
        if count1 != 0:
            for key in range(count1 - 5, count1):
                bot.send_message(message.from_user.id, links[key])
                print()
            count1 -= 5
        else:
            bot.send_message(message.from_user.id, "Вы загрузили все новости")
    log(message)
    if message.text =='Очистить':
        id_sms.append(message.id)
        for i in id_sms:
            bot.delete_message(message.chat.id, i)
            id_sms=[]

    log(message)
    print("id-sms=", id_sms)
bot.polling(none_stop=True, interval=0)
