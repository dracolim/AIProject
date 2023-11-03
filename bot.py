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
from deep_translator import GoogleTranslator
from random import seed
from random import randint

load_dotenv()
user_data = {}
response_data = {}
unique_list = [""]

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
bot.set_webhook()
WEBHOOK_HOST = 'aih-telebot-2aba1e09532a.herokuapp.com/'
WEBHOOK_PORT = int(os.environ.get('PORT', 5000))
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

r = sr.Recognizer()

@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("New Chat 🧹"))
        # Start bot introduction
        start_message = """
        Hello! 😊 how may I help you? \n*Please do not include any sensitive information (e.g. NRIC, personal information) when asking questions*
        """

        bot.send_message(message.chat.id, start_message, reply_markup=markup , parse_mode= 'Markdown') 

    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')

#text
@bot.message_handler(content_types=['text'])
def send_text(message):
    # Store the message object in user_data
    user_data[message.id] = message.text
    if message.text == "New Chat 🧹":
        res = model.getResponse(message.text)
        # hard code response

        bot.send_message(message.chat.id, res) 
    elif message.text != "New Chat 🧹":
        #give user option to choose the language first, then call the function to get RESPONSE
        voice = False
        language_buttons(voice, "" , message)  # buttons for selecting the language of the voice message


def language_buttons(voice, call , message):
    keyboard = InlineKeyboardMarkup()
    button_bu = InlineKeyboardButton(text='Burmese', callback_data='lang_burmese')
    button_ta = InlineKeyboardButton(text='Tamil', callback_data='lang_tamil')
    button_ch = InlineKeyboardButton(text='Mandarin', callback_data='lang_chinese')
    button_be = InlineKeyboardButton(text='Bengali', callback_data='lang_bengali')
    button_eng = InlineKeyboardButton(text='English', callback_data='lang_english')
    keyboard.add(button_bu, button_ta, button_ch , button_be , button_eng)

    if (voice == False): #text
        bot.send_message(message.chat.id, 'Please select a language you want your answers to convert to', reply_markup=keyboard)
    else:
        bot.send_message(call.from_user.id, 'Please select a language you want your answers to convert to', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def language_callback(call):
    print("gello")
    message_combinations = call

    if len(str(message_combinations.id)) > 6: #video
        message_id = call.message.id -1
        message = user_data[message_id]
    else: #text
        message_id = message_combinations.message_id
        message = message_combinations.text

    if message_id not in response_data and message_id != "":
        bot.send_message(call.from_user.id, "⏱️ Give me a moment ...")

        # Simulate a loading bar by sending a sequence of messages
        for i in range(1, 11):  # Assuming 10 steps in the loading bar
            progress = "▓" * i + "░" * (10 - i)
            if i // 2 == 0:
                bot.send_message(call.from_user.id, f"⌛ Progress: {progress}")
            else:
                bot.send_message(call.from_user.id, f"⏳ Progress: {progress}")
            time.sleep(5)  # Adjust the sleep time as needed

        response = model.getResponse(message)
        # response = "temp ans for testing"
        response_data[message_id] = response
    else:
        response = response_data.get(message_id)


    if call.data == 'lang_burmese':
        ans = GoogleTranslator(source="en", target="my").translate(response)
        bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_tamil':
        ans = GoogleTranslator(source="en", target="ta").translate(response)
        bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_chinese':
        ans = GoogleTranslator(source="en", target="zh-CN").translate(response)
        bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_bengali':
        ans = GoogleTranslator(source="en", target="bn").translate(response)
        bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_english':
        bot.send_message(call.from_user.id, response)  # send the heard text to the user
        _clear()


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

        language_buttons_voice(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('voice_'))
def voice_callback(call):
    print("voice...")
    text2 = ""
    if call.data == 'voice_burmese':
        text = voice_recognizer("my_MM")  # call the function with selected language
        text2 = GoogleTranslator(source="my", target="en").translate(text)
        print(text2)
        _clear()
    elif call.data == 'voice_tamil':
        text = voice_recognizer("ta_IN")  # call the function with selected language
        text2 = GoogleTranslator(source="ta", target="en").translate(text)
        _clear()
    elif call.data == 'voice_chinese':
        text = voice_recognizer("zh")  # call the function with selected language
        text2 = GoogleTranslator(source="zh-CN", target="en").translate(text)
        _clear()
    elif call.data == 'voice_bengali':
        text = voice_recognizer("bn_BD")  # call the function with selected language
        text2 = GoogleTranslator(source="bn", target="en").translate(text)
        _clear()
    elif call.data == 'voice_english':
        text = voice_recognizer("en_EN")
        text2 = text
        _clear()

    voice = True
    user_data[call.message.id] = text2
    language_buttons(voice ,call , "")

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

def language_buttons_voice(message):
    keyboard = types.InlineKeyboardMarkup()
    button_bu = InlineKeyboardButton(text='Burmese', callback_data='voice_burmese')
    button_ta = InlineKeyboardButton(text='Tamil', callback_data='voice_tamil')
    button_ch = InlineKeyboardButton(text='Mandarin', callback_data='voice_chinese')
    button_be = InlineKeyboardButton(text='Bengali', callback_data='voice_bengali')
    button_eng = InlineKeyboardButton(text='English', callback_data='voice_english')
    keyboard.add(button_bu, button_ta, button_ch , button_be , button_eng)
    bot.send_message(message.chat.id, 'Please select the voice message language.', reply_markup=keyboard)


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