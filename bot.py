import telebot

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

commands = {
    'start' :"Привет!\nЯ - бот-староста ИУ9, здесь ты можешь найти разную полезную инфу"
    'drive' :"Вот ссылка на гугл диск:\n"
    'cloud' :"Вот ссылка на облако"
}

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, commands['start'])

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
itembtn_help = telebot.types.KeyboardButton('help')
markup.add(itembtn_help)
bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)

bot.polling()