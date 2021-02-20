import telebot

TOKEN = '1670707187:AAG5e6LZGLZ8z4YO2NXMDbgvR8j4oiFJkjQ'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет!\nЯ - бот-староста ИУ9, здесь ты можешь найти разную полезную инфу")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()