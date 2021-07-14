import telebot
import config
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
mes_mnog = {'привет', 'прив', 'хай', 'здрасти', 'здравствуйте', 'здравствуй', 'здоров', 'здорова', 'здарова', 'здаров', 'приветствую', 'приветик', 'хаюшки', 'здраствуйте', 'здрастуйте', 'здратуйте'}

@bot.message_handler(commands=['start'])
def welcome(message):
    stickers_file = open('static/privet.tgs', 'rb')
    bot.send_sticker(message.chat.id, stickers_file)

    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    item3 = types.KeyboardButton("😱 Супрималор!")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                        "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                        "бот созданный, чтобы быть подопытным кроликом.".format(
                            message.from_user, bot.get_me()),
                        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def hello(message):
    if message.text in mes_mnog:
        bot.send_message(message.chat.id,
                         "Привет, {0.first_name}!\nМое имя - <b>{1.first_name}</b>, "
                         "поговорю с тобой.".format(
                             message.from_user, bot.get_me()),
                         parse_mode='html')
    elif message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)), reply_markup=types.ReplyKeyboardRemove())
        elif message.text == '😊 Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item4 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item5 = types.InlineKeyboardButton('Не очень', callback_data='bad')

            markup.add(item4, item5)

            bot.send_message(message.chat.id, 'Отлично, как у тебя? ;)', reply_markup=markup)
        elif message.text == '😱 Супрималор!':
            bot.send_message(message.chat.id, 'Щёрт, ты шо курил?))', reply_markup=types.ReplyKeyboardRemove())


        else:
            bot.send_message(message.chat.id, 'Ой, моя твоя не понимайт!')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько! 😊', reply_markup=types.ReplyKeyboardRemove())
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Жаль, могу чем-то помочь?', reply_markup=types.ReplyKeyboardRemove())

            #remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='😊 Как дела?',
                                  reply_markup=types.ReplyKeyboardRemove())

            # #show alert
            # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
            #                           text='Это тестовое уведомление')
    except Exception as e:
        print(repr(e))
# def new_line_button(message):
#     if message.chat.type == 'private':
#         if message.text == '🎲 Рандомное число':
#             bot.send_message(message.chat.id, str(random.randint(0,100)))
#         elif message.text == '😊 Как дела?':
#             bot.send_message(message.chat.id, 'Отлично, как у тебя? ;)')
#         elif message.text == '😱 Супрималор!':
#             bot.send_message(message.chat.id, 'Щёрт, ты шо курил?))')

# @bot.message_handler(content_types=['text'])
#
# def lalala(message):
#     bot.send_message(message.chat.id, message.text)
#тест
#RUN
bot.polling(none_stop=True)