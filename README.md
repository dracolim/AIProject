
# AI & Humanity Project (G2T5)
<p align="center">
<img width="138" alt="Screenshot 2023-11-07 at 1 49 25 PM" src="https://github.com/dracolim/AIProject/assets/85498185/d156137d-d222-4a32-8b27-c410eb181c67">
</p>

### Meet Potter the Chatbot
Potter is a compassionate and helpful telegram chatbot designed to serve as a friendly assistant, offering invaluable support to migrant workers as they adapt to life in Singapore. With a wealth of knowledge and resources at its virtual fingertips, Potter excels at providing migrant workers with essential information on a wide range of topics, from medical health coverage to general inquiries. Whether it's addressing healthcare concerns or answering everyday questions, Potter is committed to guiding and assisting migrant workers on their journey in Singapore.

## Run Application
1. Install dependencies
```
  pip install -r requirements.txt
```
2. Run command on terminal
```
  python bot.py
```
## Features
- Commands </br>
<img width="509" alt="Screenshot 2023-11-07 at 2 24 44 PM" src="https://github.com/dracolim/AIProject/assets/85498185/3a36bd4e-96ec-467b-b6ca-2d3b861798ea"> </br>
  1. To start the bot
     ```/start```
  2. To retrieve common asked FAQs
     ```/faq```
  3. To start a new chat and clear chat history
     ```/newchat```
- Text
    - Users can type in their questions to the bot and responses will be generated
- Voice to Text
    - Users can record their voice to ask the bot questions
    - The bot will be able to detect their voice and convert it to text , which will be fed into the Langchain Language Model to generate  responses
- Translate to other languages
   - Generated responses from the LLM can be translated to other langauges
   - Users can select out of th 5 options (English, Burmese, Tamil, Mandarin, Bengali) they wish to translate their responses to
- Application is deployed on Heroku

## Resources

- [TelegramBot Documentation](https://pypi.org/project/pyTelegramBotAPI/)
- [Langchain Documentation](https://python.langchain.com/docs/get_started/introduction)

