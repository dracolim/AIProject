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
from threading import Thread


load_dotenv()
user_data = {}
response_data = {}
unique_list = [""]
#to keep track of deletion
all_messages = {}

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)
bot.set_webhook()
WEBHOOK_HOST = 'aih-telebot-2aba1e09532a.herokuapp.com/'
WEBHOOK_PORT = int(os.environ.get('PORT', 5000))
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

r = sr.Recognizer()

#FAQ SECTION
mental_health_FAQ = """
*🧠 Common Mental Health FAQs*\n
*Q1: Are there mental health services available for migrant workers?*
Yes, there are services like HealthServe, which offers a mental health and counselling service team, a 24-hour crisis helpline, and large group psychoeducation workshops.\n
*Q2: How do recent issues impact the physical and mental well-being of migrant workers?*
Issues such as substandard living conditions, poor nutrition, excessive physical demands, coercive work practices, and social exclusion have adverse effects on migrant workers' mental and physical health.\n
"""
dental_FAQ = """
*🦷 Common Dental FAQs*\n
*Q1: What does the dental coverage for migrant workers entail?*
The Migrant Workers’ Centre (MWC) offers an associate membership program that provides dental services at a flat fee of up to $30, with a $5 discount for associate members.\n
"""
injury_FAQ = """
*🤕 Common Injury-related FAQs*\n
*Q1: How should a migrant worker in the construction industry proceed if they suffer an injury while working?*
They should seek medical help, inform their employer immediately, provide medical certificates and bills to their employer, and ensure the employer notifies the Ministry of Manpower (MOM) of the incident for Work Injury Compensation Act (WICA) processing.\n 
*Q2: How can a Tamil-speaking migrant worker understand what to do if injured on the job?*
A Tamil translation of the procedure is available which guides the worker to seek medical help, inform their employer, submit medical documents, and follow up to ensure that the incident is reported to MOM for WICA processing.\n
"""
medical_FAQ = """
*🩺 Common Medical Healthcare FAQs*\n
*Empty*
"""
coverage_FAQ = """
*💲 Common Healthcare coverage FAQs*\n
*Q1: What type of healthcare coverage is available for migrant workers in Singapore?*
Migrant workers have mandatory medical insurance coverage for hospitalisation expenses, including non-work related injuries or illnesses. Coverage limits vary based on the purchase date of the insurance policy. The Primary Care Plan (PCP) is also available to provide quality, accessible, and affordable primary care.\n
*Q2: Under what criteria might migrant workers be asked to co-pay for healthcare services?*
Co-payment is subject to conditions such as the amount not exceeding 10% of the worker's monthly salary, the duration not exceeding 6 months, and the co-payment option being stated in the employment contract or received collective agreement.\n
*Q3: What is the role of the Primary Care Plan (PCP) in migrant workers' healthcare?*
The PCP aims to provide accessible and affordable primary care, support public health surveillance, and offer peace of mind for both employers and migrant workers.\n
*Q4: How do the healthcare coverages under EFMA, WICA, and EA compare?*
The EFMA mandates employers to cover medical treatment costs and purchase medical insurance. WICA allows workers to file a claim if they suffer a work-related injury or disease. The EA requires employers to provide paid sick leave, including dental leave if certified by a designated doctor.\n
"""
others_FAQ = """
*⛑️ Common Others FAQs*\n
*Q1: What barriers do migrant workers face in accessing healthcare?*
Migrant workers may face barriers such as cultural and language differences, financial constraints, lack of knowledge about the healthcare system, limited healthcare coverage, social and structural barriers, and work-related barriers such as long working hours.\n\n
"""


@bot.message_handler(commands=['start'])
def start(message):
    """
    Bot will introduce itself upon /start command, and prompt user for his request
    """
    try:
        # Start bot introduction
        start_message = """
        Hello! 😊 how may I help you? \n*❗️Please do not include any sensitive information (e.g. NRIC, personal information) when asking questions*\n\n📋 Commands: \n/start - To start the bot\n/faq - Commonly asked questions and answers\n/newchat - Start a new chat
        """
        
        message3 = bot.send_message(message.chat.id, start_message, parse_mode= 'Markdown')

        message_id = message3.message_id
        chat_id = message.chat.id
            
        all_messages[message_id] = chat_id

        # SET MENU BAR
        c1 = BotCommand(command='start', description='Start the Bot')
        c2 = BotCommand(command='faq', description='Commonly asked questions and answers')
        c3 = BotCommand(command='newchat', description='Start a new chat')
        bot.set_my_commands([c1,c2,c3])
        bot.set_chat_menu_button(message.chat.id, MenuButtonCommands('commands'))
        
    except Exception as e:
        bot.send_message(message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')
        

@bot.message_handler(commands=['faq'])
def commonFAQ(message):
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(KeyboardButton("🧠 Mental Health"), KeyboardButton("🦷 Dental"))
        markup.row(KeyboardButton("🤕 Injury"), KeyboardButton("🩺 Medical Health"))
        markup.row(KeyboardButton("💲 Healthcare coverage"), KeyboardButton("⛑️ Others"))

        FAQ_question = """
        Please *select* the category you want to know more about on the pop up keyboard
        """
        
        message3 = bot.send_message(message.chat.id, FAQ_question ,reply_markup=markup, parse_mode= 'Markdown')

        message_id = message3.message_id
        chat_id = message.chat.id
            
        all_messages[message_id] = chat_id
        
    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')

@bot.message_handler(commands=['newchat'])
def commonFAQ(message):
    try:
        #calling response model
        res = model.getResponse("new chat")

        message3 = bot.send_message(message.chat.id, res)

        message_id = message3.id
        chat_id = message.chat.id
            
        all_messages[message_id] = chat_id

        for each in all_messages:
            bot.delete_message(all_messages[each], each)
            del each

        all_messages.clear()
        
        message3 = bot.send_message(message.chat.id, res , parse_mode= 'Markdown')
        message_id = message3.message_id
        chat_id = message.chat.id
        all_messages[message_id] = chat_id
        
    except Exception as e:
        bot.send_message(
            message.chat.id, 'Sorry, something seems to gone wrong! Please try again later!')

#text
@bot.message_handler(content_types=['text'])
def send_text(message):
    isItVoice = True
    if message.text == "🧠 Mental Health":
        message3 = bot.send_message(message.chat.id, mental_health_FAQ, parse_mode= 'Markdown')
    elif message.text == "🦷 Dental":
        message3 = bot.send_message(message.chat.id, dental_FAQ, parse_mode= 'Markdown')
    elif message.text == "🤕 Injury":
        message3 = bot.send_message(message.chat.id, injury_FAQ, parse_mode= 'Markdown')
    elif message.text == "🩺 Medical Health":
        message3 = bot.send_message(message.chat.id, medical_FAQ, parse_mode= 'Markdown')
    elif message.text == "💲 Healthcare coverage":
        message3 = bot.send_message(message.chat.id, coverage_FAQ, parse_mode= 'Markdown')
    elif message.text == "⛑️ Others":
        message3 = bot.send_message(message.chat.id, others_FAQ, parse_mode= 'Markdown')
    else:
        #give user option to choose the language first, then call the function to get RESPONSE
        voice = False
        isItVoice = False
        language_buttons(voice, "" , message)  # buttons for selecting the language of the voice message

    #for storing purposes
    if isItVoice == True:
        message_id = message3.message_id
        chat_id = message.chat.id

        all_messages[message_id] = chat_id


def language_buttons(voice, call , message):
    keyboard = InlineKeyboardMarkup()
    button_bu = InlineKeyboardButton(text='Burmese', callback_data='lang_burmese')
    button_ta = InlineKeyboardButton(text='Tamil', callback_data='lang_tamil')
    button_ch = InlineKeyboardButton(text='Mandarin', callback_data='lang_chinese')
    button_be = InlineKeyboardButton(text='Bengali', callback_data='lang_bengali')
    button_eng = InlineKeyboardButton(text='English', callback_data='lang_english')
    keyboard.add(button_bu, button_ta, button_ch , button_be , button_eng)

    if (voice == False): #text
        message3 = bot.send_message(message.chat.id, 'Please select a language you want your answers to convert to', reply_markup=keyboard)
        message_id = message3.message_id
        chat_id =  message.chat.id

        all_messages[message_id] = chat_id

    else:
        message3 = bot.send_message(call.from_user.id, 'Please select a language you want your answers to convert to', reply_markup=keyboard)
        message_id =  message3.message_id
        chat_id =  call.from_user.id

        all_messages[message_id] = chat_id


def printLoading(call):
    message3 = bot.send_message(call.from_user.id, "⏱️ Give me a moment ...").message_id
        
    message_id2 =  message3
    chat_id =  call.from_user.id

    all_messages[message_id2] = chat_id

    # Simulate a loading bar by sending a sequence of messages
    for i in range(1, 10):  # Assuming 10 steps in the loading bar
        progress = "▓" * i + "░" * (10 - i)
        if i // 2 == 0:
            message3 = bot.send_message(call.from_user.id, f"⌛ Progress: {progress}").message_id
        else:
            message3 = bot.send_message(call.from_user.id, f"⏳ Progress: {progress}").message_id
        time.sleep(25)  # Adjust the sleep time as needed

        message_id2 =  message3
        chat_id =  call.from_user.id
        all_messages[message_id2] = chat_id

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
        response = model.getResponse(message)
        response_data[message_id] = response
    else:
        response = response_data.get(message_id)


    if call.data == 'lang_burmese':
        ans = GoogleTranslator(source="en", target="my").translate(response)
        message3  = bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_tamil':
        ans = GoogleTranslator(source="en", target="ta").translate(response)
        message3  = bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_chinese':
        ans = GoogleTranslator(source="en", target="zh-CN").translate(response)
        message3  = bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_bengali':
        ans = GoogleTranslator(source="en", target="bn").translate(response)
        message3  = bot.send_message(call.from_user.id, ans)  # send the heard text to the user
        _clear()
    elif call.data == 'lang_english':
        message3 = bot.send_message(call.from_user.id, response)  # send the heard text to the user
        _clear()
    
    message_id =  message3.message_id
    chat_id =  call.from_user.id

    all_messages[message_id] = chat_id


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

    message_id2 = message.id
    chat_id = message.chat.id
    all_messages[message_id2] = chat_id



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

    message_id = message.id
    chat_id = message.chat.id
    all_messages[message_id] = chat_id
        

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