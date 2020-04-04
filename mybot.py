import json
import random

from pip._vendor import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,MessageHandler,Filters
import logging
import html

updater = Updater(token='1006575555:AAEuRhycYN78jf-iEBhMIQlev0A9O2Cu4kw', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello , I am a telegram bot !')


def pin(update, context):
    msg = context.bot.send_message(chat_id=update.effective_chat.id, text='pin is running !')
    context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=msg.message_id)


def filter(update, context):
    filter_set=['zalo', 'tiền', 'đụ']
    text=update.message.text
    for t in filter_set:
        if t in text:
            context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.message.message_id)





def get_url():
    content = 'https://random.dog/woof.json'
    get = requests.get(content).json()
    url = get['url']
    return url


def get_question():
    url = 'https://opentdb.com/api.php?amount=1&category=18&type=multiple'
    get_data = requests.get(url).json()
    quest = html.unescape(get_data['results'][0]['question'])
    correct_answer = html.unescape(get_data['results'][0]['correct_answer'])
    answ_set = get_data['results'][0]['incorrect_answers']
    answ_set.insert(random.randint(0, 2), correct_answer)
    return quest, correct_answer, answ_set


def dog(update, context):
    url = get_url()
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=url, caption='this is a random dog picture')


def question(update, context):
    data = get_question()
    q = data[0]
    correct_answer = data[1]
    keyboard = [[InlineKeyboardButton(text=html.unescape(data[2][0]),
                                      callback_data=str(data[2][0]) + ' is correct answer' if data[2][
                                                                                                  0] == correct_answer else str(
                                          data[2][0]) + ' is incorrect answer')],
                [InlineKeyboardButton(text=html.unescape(data[2][1]),
                                      callback_data=str(data[2][1]) + ' is correct answer' if data[2][
                                                                                                  1] == correct_answer else str(
                                          data[2][1]) + ' is incorrect answer')],
                [InlineKeyboardButton(text=html.unescape(data[2][2]),
                                      callback_data=str(data[2][2]) + ' is correct answer' if data[2][
                                                                                                  2] == correct_answer else str(
                                          data[2][2]) + ' is incorrect answer')],
                [InlineKeyboardButton(text=html.unescape(data[2][3]),
                                      callback_data=str(data[2][3]) + ' is correct answer' if data[2][
                                                                                                  3] == correct_answer else str(
                                          data[2][3]) + ' is incorrect answer')]
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text=q)
    update.message.reply_text('Choose the correct answer:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    query.edit_message_text(text=query.data)


def __main__():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    pin_handler = CommandHandler('pin', pin)
    dispatcher.add_handler(pin_handler)

    dog_handler = CommandHandler('dog', dog)
    dispatcher.add_handler(dog_handler)

    question_handler = CommandHandler('question', question)
    dispatcher.add_handler(question_handler)

    filter_handler = MessageHandler(Filters.text, filter)
    dispatcher.add_handler(filter_handler)

    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()


if __name__ == "__main__":
    __main__()
