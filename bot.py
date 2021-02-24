import telebot
import time
#This file with dict of commands I decided not to add to repo
import Data

with open('token.txt', 'r') as f:
    TOKEN = f.readline()

knownUsers = []
userStep = {}
help_text = ''

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
            print(str(m.chat.username) + " " + "||" + time.strftime("%m/%d/%Y, %H:%M:%S", time.gmtime(m.date)) + "||" +
                  " [" + str(m.chat.id) + "]: " + m.text)

markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
help_btn = telebot.types.KeyboardButton('HELP')
cloud_btn = telebot.types.KeyboardButton('ОБЛАКО')
drive_btn = telebot.types.KeyboardButton('ДИСК')
eu_btn = telebot.types.KeyboardButton('ЭУ')
timetable_btn = telebot.types.KeyboardButton('РАСПИСАНИЕ')
dene_btn = telebot.types.KeyboardButton('ЗАМДЕК')
diff_btn = telebot.types.KeyboardButton('ДУ инфо')
subject_btn = telebot.types.KeyboardButton('ПРЕДМЕТЫ И ФИО ПРЕПОДОВ')
homework_btn = telebot.types.KeyboardButton('ДЗ')

markup.add(help_btn, eu_btn, cloud_btn, drive_btn, diff_btn, subject_btn)
markup.add(homework_btn)

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)

def give_markup(cid):
    bot.send_message(cid, 'Возвращаемся', reply_markup=markup)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    unique = ''
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = 0
        #Just sume cute feature
        if m.from_user.username == Data.myLove:
            unique = ', солнце'
        bot.send_message(cid, "Привет" + unique + "!\nЯ бот-староста группы ИУ9-41Б")
        command_help(m)
    else:
        bot.send_message(cid, "Я тебя уже знаю")

@bot.message_handler(commands=['secret'])
def command_love(m):
    cid = m.chat.id
    if m.from_user.username == Data.myLove:
        bot.send_message(cid, Data.letter)
    else:
        bot.send_message(cid, 'Я не знаю как ты это нашёл, но это не для тебя и иди нахуй')

@bot.message_handler(func=lambda message: message.text in ['/help', 'HELP'])
def command_help(m):
    cid = m.chat.id
    help_text = "Вот что я могу: \n"
    for key, value in Data.data.items():
        help_text += key + ": "
        help_text += value['info'] + "\n"
    help_text += 'По поводу вопросов, багов и предложений писать сюда @rizh42'
    bot.send_message(cid, help_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['/subjects', 'ПРЕДМЕТЫ И ФИО ПРЕПОДОВ'])
def command_subjects(m):
    cid = m.chat.id
    keys = ''
    for key in list(Data.data['ПРЕДМЕТЫ']['data'].keys()):
        keys += key + ' ' + Data.data['ПРЕДМЕТЫ']['data'][key] + '\n'
    bot.send_message(cid, keys)

@bot.message_handler(func=lambda message: message.text in ['/drive', 'ДИСК'])
def command_drive(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на гугл диск:\n' + Data.data['ДИСК']['data'])

@bot.message_handler(func=lambda message: message.text in ['/cloud', 'ОБЛАКО'])
def command_cloud(m):
    cid = m.chat.id
    bot.send_message(cid, 'Ссылка на облако:\n' + Data.data['ОБЛАКО']['data'])

@bot.message_handler(func=lambda message: message.text in ['/dene', 'ЗАМДЕК'])
def command_dene(m):
    cid = m.chat.id
    bot.send_message(cid, Data.data['ЗАМДЕК']['data'])

@bot.message_handler(func=lambda message: message.text in ['/eu', 'ЭУ'])
def command_eu(m):
    cid = m.chat.id
    bot.send_message(cid, 'Вот твоя ссылка на ЭУ:\n' + Data.data['ЭУ']['data'])

@bot.message_handler(func=lambda message: message.text in ['/timetable', 'РАСПИСАНИЕ'])
def command_timetable(m):
    cid = m.chat.id
    bot.send_message(cid, 'Вот твоё расписание:\n')
    bot.send_photo(cid, open(Data.data['РАСПИСАНИЕ']['data'], 'rb'))

@bot.message_handler(func=lambda message: message.text in ['/diff', 'ДУ инфо'])
def command_diff(m):
    cid = m.chat.id
    bot.send_message(cid, Data.data['ДУ инфо']['data'])

@bot.message_handler(func=lambda message: message.text in ['/hw', 'ДЗ'])
def command_hw(m):
    cid = m.chat.id
    hw_markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    for key in Data.data['ДЗ']['data']:
        hw_markup.add(telebot.types.KeyboardButton(key))
    bot.send_message(cid, 'Выбери предмет', reply_markup=hw_markup)

@bot.message_handler(func=lambda message: message.text in ['ДГМА', 'ДУ ДЗ', 'КомплАн', 'Компьютерная графика', 'Алгебра', 'ОС'])
def command_hw_subj(m):
    cid = m.chat.id
    bot.send_message(cid, Data.data['ДЗ']['data'][m.text])
    give_markup(cid)

@bot.message_handler(commands=['add_hw'])
def command_add_hw(m):
    txt = m.text.split(' ')
    print(txt[2:])
    name = txt[1]
    hw = ''
    for item in txt[2:]:
        hw += item + ' '
    tmp = {name:hw}
    Data.data['ДЗ']['data'].update(tmp)
    

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    if m.from_user.username == Data.myLove:
        bot.send_message(m.chat.id, "I love you <3\nЛучше напиши мне в личку)))\nНу или ты неправильно воспользовалась командой)))")
    else:
        bot.send_message(m.chat.id, "Ты дурак или да?\nВызови /help чтоб вспомнить что я могу!")

bot.polling(none_stop=True)