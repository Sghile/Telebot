import telebot
import const
import vk_api


bot = telebot.TeleBot(const.tokenTele)
vk_session = vk_api.VkApi(token=const.token)
vk = vk_session.get_api()

tools = vk_api.VkTools(vk_session)
friends = tools.get_all('friends.search', 90)


def log(message):
    from datetime import datetime
    print(datetime.now())
    print(message.from_user.first_name, message.from_user.last_name, str(message.from_user.id), message.text)


@bot.message_handler(commands=['start'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('А токен на гитхаб не залил?', 'Узнать мой tg id')
    user_markup.row('oh shit. I am sorry!', '/help')
    user_markup.row('Загрузить моих друзей из VK')
    user_markup.row('/start', '/stop')
    bot.send_message(message.from_user.id, "Привет!", reply_markup=user_markup)
    log(message)


@bot.message_handler(commands=['stop'])
def handel_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True)
    bot.send_message(message.from_user.id, 'meh', reply_markup=hide_markup)
    log(message)


@bot.message_handler(commands=['help'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop')
    bot.send_message(message.from_user.id, "Нажмите Загрузить друзей, после выберите друга и напишите ему сообщение",
                     reply_markup=user_markup)
    log(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Пошёл нахуй отсюда(не знать тебе токена)':
        bot.send_sticker(message.from_user.id, "CAADBAADVgADgFwlA4KN7F0OMsfZAg")
        log(message)

    elif message.text == 'Узнать мой tg id':
        if message.from_user.id == const.my_id:
            bot.send_message(message.from_user.id, 'Избранный')
        else:
            bot.send_message(message.from_user.id, message.from_user.id)
        log(message)
    elif message.text == 'oh shit. I am sorry!':
        bot.send_sticker(message.from_user.id, "CAADBAADNQMAAkMxogY12wEWrMirqgI")

    elif message.text == 'Назад':
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row('Пошёл нахуй отсюда(не знать тебе токена)', 'Узнать мой tg id')
        user_markup.row('oh shit. I am sorry!')
        user_markup.row('Загрузить моих друзей из VK')
        user_markup.row('/stop', '/help')
        bot.send_message(message.from_user.id, "Как скажешь.", reply_markup=user_markup)

    elif message.text == 'Загрузить моих друзей из VK':
        if message.from_user.id == const.my_id:
            log(message)
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            item = telebot.types.KeyboardButton('Назад')
            user_markup.add(item)
            for i in range(len(friends['items'])):
                item = telebot.types.KeyboardButton(friends['items'][i]['first_name'] + ' ' +
                                                    friends['items'][i]['last_name'])
                user_markup.add(item)
            bot.send_message(message.from_user.id, "Выберите друга!", reply_markup=user_markup)
        else:
            bot.send_sticker(message.from_user.id, "CAADBAADsgADgFwlAx7zizgz_W5GAg")

    elif message.text == find_friend(friends, message.text):
        global friend_id
        if message.from_user.id == const.my_id:
            friend_id = find_friend_id(friends, message.text)
            bot.send_message(message.from_user.id, 'Введи сообщение:')
        else:
            bot.send_sticker(message.from_user.id, "CAADBAADsgADgFwlAx7zizgz_W5GAg")
        log(message)

    elif message == message:
        if message.from_user.id == const.my_id:
            if friend_id == 0:
                bot.send_message(message.from_user.id, 'Выбери друга!')
            else:
                vk.messages.send(user_id=friend_id, message=message.text)
                friend_id = 0
        else:
            bot.send_sticker(message.from_user.id, "CAADBAADsgADgFwlAx7zizgz_W5GAg")
        log(message)


def find_friend(friends, message):
    for q in range(len(friends['items'])):
        if message == friends['items'][q]['first_name'] + ' ' + friends['items'][q]['last_name']:
            return message


def find_friend_id(friends, message):
    for q in range(len(friends['items'])):
        if message == friends['items'][q]['first_name'] + ' ' + friends['items'][q]['last_name']:
            return friends['items'][q]['id']


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
