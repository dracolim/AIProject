import telebot
import os
from dotenv import load_dotenv
import model
import traceback
import speech_recognition as sr
import subprocess
from telebot import *
from telebot.types import *
from requests import *
from telegram.ext import *

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
bot.set_webhook()
r = sr.Recognizer()

@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Clear Chat 🧹'))

        # Start bot introduction
        start_message = "Hello! Ask me anything about life in Singapore, or if you need help! \n"

        bot.send_message(message.chat.id, start_message, reply_markup=markup)

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')

#text
@bot.message_handler(content_types=['text'])
def send_text(message):
    response = model.getResponse(message.text)
    bot.send_message(message.chat.id, response)

#voice
@bot.message_handler(content_types=['voice'])
def voice_handler(message):
    file_id = message.voice.file_id  # file size check. If the file is too big, FFmpeg may not be able to handle it.
    file = bot.get_file(file_id)

    file_size = file.file_size
    if int(file_size) >= 715000:
        bot.send_message(message.chat.id, 'Upload file size is too large.')
    else:
        download_file = bot.download_file(file.file_path)  # download file for processing
        with open('audio.ogg', 'wb') as file:
            file.write(download_file)

        language_buttons(message)  # buttons for selecting the language of the voice message

@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.data == 'russian':
        text = voice_recognizer('ru_RU')  # call the function with selected language
        bot.send_message(call.from_user.id, text)  # send the heard text to the user
        _clear()
    elif call.data == 'english':
        text = voice_recognizer('en_EN')
        bot.send_message(call.from_user.id, text)
        _clear()

def voice_recognizer(language):
    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = r.record(source)  # listen to file
            text = r.recognize_google(audio, language=language)  # and write the heard text to a text variable
        except:
            logger.error(f"Exception:\n {traceback.format_exc()}")

    return text

def language_buttons(message):
    keyboard = InlineKeyboardMarkup()
    button_ru = InlineKeyboardButton(text='Russian', callback_data='russian')
    button_eng = InlineKeyboardButton(text='English', callback_data='english')
    keyboard.add(button_ru, button_eng)
    bot.send_message(message.chat.id, 'Please select a voice message language.', reply_markup=keyboard)

def _clear():
    """Remove unnecessary files"""
    _files = ['audio.wav', 'audio.ogg']
    for _file in _files:
        if os.path.exists(_file):
            os.remove








def main():
    """Runs the Telegram Bot"""
    print('Loading configuration...') # Perhaps an idea on what you may want to change (optional)
    print('Successfully loaded! Starting bot...')
    bot.infinity_polling()


if __name__ == '__main__':
    main()