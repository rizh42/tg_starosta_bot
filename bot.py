import telebot
#This file with dict of commands I decided not to add to repo
import data

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
    'dene': 'Расписание зам. декана',
    'diff': 'Ссылка на лекцию и диск по ДУ',
    'teacher \'имя предмета\'' :'Список ФИО всех преподов',
    'subjects' :'Список имен предметов для предыдущей комманды'
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
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    unique = ''
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        #Just sume cute feature
        if m.from_user.username == 'maslerk':
            unique = ', солнце'
        bot.send_message(cid, "Привет" + unique + "!\nЯ бот-староста группы ИУ9-41Б")
        command_help(m)
    else:
        bot.send_message(cid, "Я тебя уже знаю")


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я могу: \n"
    for key in commands_help:  
        help_text += "/" + key + ": "
        help_text += commands_help[key] + "\n"
    help_text += 'По поводу вопросов, багов и предложений писать сюда @rizh42'
    bot.send_message(cid, help_text)

@bot.message_handler(commands=['subjects'])
def command_subjects(m):
    cid = m.chat.id
    keys = ''
    for key in list(data.teachers.keys()):
        keys += key+'\n'
    bot.send_message(cid, keys)

@bot.message_handler(commands=['teacher'])
def command_teacher(m):
    cid = m.chat.id
    text = m.text.split(" ")
    if len(text) > 1 and text[0] == '/teacher':
        bot.send_message(cid, data.teachers[text[1]])
    else:
        bot.send_message(cid, 'Видимо, ты неправильно использовал эту комманду, перечитай /help и попробуй ещё раз!')

@bot.message_handler(commands=['drive'])
def command_drive(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на гугл диск:\n' + data.commands['drive'])

@bot.message_handler(commands=['cloud'])
def command_cloud(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на облако:\n' + data.commands['cloud'])

@bot.message_handler(commands=['dene'])
def command_dene(m):
    cid = m.chat.id
    bot.send_message(cid, data.commands['dene'])

@bot.message_handler(commands=['eu'])
def command_eu(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на Электронный Университет:\n' + data.commands['eu'])

@bot.message_handler(commands=['timetable'])
def command_timetable(m):
    cid = m.chat.id
    bot.send_message(cid, 'Вот твоё расписание:\n')
    bot.send_photo(cid, open(data.commands['timetable'], 'rb'))

@bot.message_handler(commands=['diff'])
def command_diff(m):
    cid = m.chat.id
    bot.send_message(cid, 'Диск с записями лекций:\n' + data.commands['diff']['drive'] + data.commands['diff']['zoom'])

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    if m.from_user.username == 'maslerk':
        bot.send_message(m.chat.id, "I love you <3\nЛучше напиши мне в личку)))")
    else:
        bot.send_message(m.chat.id, "Ты дурак или да?\nВызови /help чтоб вспомнить что я могу!")

bot.polling(none_stop=True)