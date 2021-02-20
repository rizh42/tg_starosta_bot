import telebot
import commands

with open('token.txt', 'r') as f:
    TOKEN = f.readline()

knownUsers = []
userStep = {}

commands_help = {
    'help': "Что могу",
    'drive': "Ссылка на гугл диск",
    'cloud': "Ссылка на облако",
    'eu': 'ЭУ',
    'timetable': 'Расписание',
    'dene': 'Расписание зам. декана'
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
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, "Привет!\nЯ бот-староста группы ИУ9-41Б")
        command_help(m)
    else:
        bot.send_message(cid, "Я тебя уже знаю")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я могу: \n"
    for key in commands_help:  # generate help text out of the commands_help dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands_help[key] + "\n"
    help_text += 'По поводу вопросов, багов и предложений писать сюда @rizh42'
    bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['drive'])
def command_drive(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на гугл диск:\n' + commands.cmds['drive'])

@bot.message_handler(commands=['cloud'])
def command_cloud(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на облако:\n' + commands.cmds['cloud'])

@bot.message_handler(commands=['dene'])
def command_dene(m):
    cid = m.chat.id
    bot.send_message(cid, commands.cmds['dene'])

@bot.message_handler(commands=['eu'])
def command_eu(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на Электронный Университет:\n' + commands.cmds['eu'])

@bot.message_handler(commands=['timetable'])
def command_timetable(m):
    cid = m.chat.id
    bot.send_message(cid, 'Вот твоё расписание:\n')
    bot.send_photo(cid, open(commands.cmds['timetable'], 'rb'))

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    bot.send_message(m.chat.id, "Ты дурак или да?\nВызови /help чтоб вспомнить что я могу!")


bot.polling()
