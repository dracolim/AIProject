# AI & Humanity Project (G2T5)
![example workflow](https://img.shields.io/badge/Build%20in-Python-blue)
![example workflow](https://img.shields.io/badge/Deployed%20in-Heroku-green)
![example workflow](https://img.shields.io/badge/LLM%20Langchain-red)
<p align="center">
<img width="140" alt="Screenshot 2023-11-08 at 5 49 23 PM" src="https://github.com/dracolim/AIProject/assets/85498185/8ced2cc9-6af0-4672-a221-3bc0b8dd3d91">
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
<img width="500" alt="Screenshot 2023-11-08 at 5 59 00 PM" src="https://github.com/dracolim/AIProject/assets/85498185/54c2dbb3-a208-448e-8ae3-30636a3b3beb"> </br>
  1. ```/start``` - To start the bot
  2. ```/faq``` - To retrieve common asked FAQs </br>
     <img width="500" alt="Screenshot 2023-11-08 at 5 55 33 PM" src="https://github.com/dracolim/AIProject/assets/85498185/2c0e3133-94ec-4e75-9797-ff84f4064547">
  4. ```/newchat``` - To start a new chat and clear chat history </br>
     <img width="500" alt="Screenshot 2023-11-08 at 5 56 24 PM" src="https://github.com/dracolim/AIProject/assets/85498185/dc64f729-fc7d-49b6-8d97-62519ee07b0c">
- Text
    - Users can input their questions for the bot and the bot will generate responses
      <img width="500" alt="Screenshot 2023-11-08 at 5 50 47 PM" src="https://github.com/dracolim/AIProject/assets/85498185/ea632bd7-5982-4178-977f-a8c5714f04e1">
- Voice to Text
    - Users can record their voice to ask questions to the bot
    - It can detect their voicse and convert it to text , which will be fed into the Langchain Language Model to generate responses
      <img width="500" alt="Screenshot 2023-11-08 at 5 54 39 PM" src="https://github.com/dracolim/AIProject/assets/85498185/06392ba1-367c-489d-ac3b-1bc2bd26fbdb">
- Translate to different languages
   - Generated responses from the LLM can be translated to various langauges
   - Users can chooses from the 5 options (English, Burmese, Tamil, Mandarin, Bengali) they wish to translate their responses
     <img width="500" alt="Screenshot 2023-11-08 at 5 51 41 PM" src="https://github.com/dracolim/AIProject/assets/85498185/121c1bba-d975-429e-978d-e88995eba968">
- Application is deployed on Heroku
  - The application is hosted and deployed on Heroku

## Resources
- [TelegramBot Documentation](https://pypi.org/project/pyTelegramBotAPI/)
- [Langchain Documentation](https://python.langchain.com/docs/get_started/introduction)

