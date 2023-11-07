
# AI & Humanity Project (G2T5)
![example workflow](https://img.shields.io/badge/Build%20in-Python-blue)
![example workflow](https://img.shields.io/badge/Deployed%20in-Heroku-green)
![example workflow](https://img.shields.io/badge/LLM%20Langchain-red)
<p align="center">
<img width="138" alt="Screenshot 2023-11-07 at 1 49 25 PM" src="https://github.com/dracolim/AIProject/assets/85498185/d156137d-d222-4a32-8b27-c410eb181c67">
</p>

### Meet Potter the Chatbot
Potter is a compassionate and helpful telegram chatbot designed to serve as a friendly assistant, offering invaluable support to Healthserve's volunteers to help migrant workesr adapt to life in Singapore. With a wealth of knowledge and resources at its virtual fingertips, Potter excels at providing volunteers with essential information on a wide range of topics, from medical health coverage to general inquiries. Whether it's addressing healthcare concerns or answering everyday questions, Potter is committed to guiding and assisting volunteers in supporting migrant workers on their journey in Singapore.

## Run Application
**To use the bot**
1. Go to telegram App
2. Search telegram username @IWillHelpYouBot
3. Good to go!
   
**To run Locally**
1. Install dependencies
```
  pip install -r requirements.txt
```
2. Run command on terminal
```
  python bot.py
```
If everything works, it should produce the following:
```
Loading configuration...
Successfully loaded! Starting bot...
```

## Features
- Commands </br>
<img width="509" alt="Screenshot 2023-11-07 at 2 24 44 PM" src="https://github.com/dracolim/AIProject/assets/85498185/3a36bd4e-96ec-467b-b6ca-2d3b861798ea"> </br>
  1. ```/start``` - To start the bot
  2. ```/faq``` - To retrieve common asked FAQs
  3. ```/newchat``` - To start a new chat and clear chat history
- Text
    - Users can input their questions for the bot and the bot will generate responses
- Voice to Text
    - Users can record their voice to ask questions to the bot
    - It can detect their voicse and convert it to text , which will be fed into the Langchain Language Model to generate responses
- Translate to different languages
   - Generated responses from the LLM can be translated to various langauges
   - Users can chooses from the 5 options (English, Burmese, Tamil, Mandarin, Bengali) they wish to translate their responses
- Application is deployed on Heroku
  - The application is hosted and deployed on Heroku

## Resources

- [TelegramBot Documentation](https://pypi.org/project/pyTelegramBotAPI/)
- [Langchain Documentation](https://python.langchain.com/docs/get_started/introduction)

