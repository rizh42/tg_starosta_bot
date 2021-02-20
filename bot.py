import telebot
import commands

TOKEN = ''

with open('token.txt', 'r') as f:
    TOKEN = f.readline()

# print(TOKEN)

knownUsers = []
userStep = {}

commands_help = {
    # 'start' :"Привет!\nЯ - бот-староста ИУ9, здесь ты можешь найти разную полезную инфу",
    'drive': "Ссылка на гугл диск",
    'cloud': "Ссылка на облако",
    'eu': 'ЭУ',
    'timetable': 'Расписание'
}

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        # save user id, so you could brodcast messages to all users of this bot later
        knownUsers.append(cid)
        # save user id and his current "command level", so he can use the "/getImage" command
        userStep[cid] = 0
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(
            cid, "I already know you, no need for me to scan you again!")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я могу: \n"
    for key in commands_help:  # generate help text out of the commands_help dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands_help[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(func=lambda message: True)
def command(message):
    bot.reply_to(message, message.text)


markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
itembtn_help = telebot.types.KeyboardButton('help')
markup.add(itembtn_help)
#bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)

bot.polling()
