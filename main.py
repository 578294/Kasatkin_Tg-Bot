import telebot
import sqlite3
import messages
from peewee import *
from config import TOKEN
bot = telebot.TeleBot(TOKEN)
CLIENTS_INFO = {

}

@bot.message_handler(commands=["start"])
def welcome(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=messages.button_DimIl)
    button2 = telebot.types.KeyboardButton(text=messages.button_POPUTI)
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(
        chat_id,
        "Здравствуйте! Уточните, пожалуйста, вас интересует? ",
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, answer)


def answer(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    if message.text == messages.button_DimIl:
        bot.send_message(chat_id, messages.button_booking_guest_info)
        answer_button_check_in(message)
    elif message.text == messages.button_POPUTI:
        bot.send_message(chat_id, messages.button_info_POPUTI)
    else:
        print('Неверный формат сообщения')

def answer_button_check_in(message: telebot.types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_check_in)
    CLIENTS_INFO[chat_id]['enter_date'] = message.text
    bot.register_next_step_handler(message, answer_button_check_out)

def answer_button_check_out(message: telebot.types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_check_out)
    CLIENTS_INFO[chat_id] = {}
    CLIENTS_INFO[chat_id]['out_date'] = message.text
    print(message.text)
    bot.register_next_step_handler(message, answer_button_adults)

def answer_button_adults(message: telebot.types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_adults)
    CLIENTS_INFO[chat_id]['adult'] = message.text
    print(message.text)
    bot.register_next_step_handler(message, answer_button_children)

def answer_button_children(message: telebot.types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_children)
    CLIENTS_INFO[chat_id]['children'] = message.text
    print(message.text)
    bot.send_message(chat_id, messages.message_about_DimIL)


# connection = sqlite3.connect('database_Dimil.db')
db = SqliteDatabase('database_Dimil.db')

class TDIMIL(Model):
    client_name = CharField(unique=True)
    button_phone_number = CharField()
    button_flexible_date = CharField()
    button_check_in = CharField()
    button_check_out = CharField()
    button_adults = CharField()
    button_children = CharField()

    class Meta:
        database = db


TDIMIL.create_table()

# Создаем таблицу database_Dimil
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS database_Dimil (
# id INTEGER PRIMARY KEY,
# client_name TEXT NOT NULL,
# button_phone_number TEXT NOT NULL,
# button_flexible_date  TEXT NOT NULL,
# button_check_in TEXT NOT NULL,
# button_check_out TEXT NOT NULL,
# button_adults TEXT NOT NULL,
# button_children TEXT NOT NULL
# )
# ''')



#cursor.execute('INSERT INTO database_Dimil (id, client_name, button_phone_number, button_check_in, button_check_out, button_flexible_date) VALUES (?, ?, ?, ?, ?, ?)', ('newuser', 'newuser@example.com', 28))



if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()


#@bot.message_handler(func=lambda message: message.text == "Здравствуйте! Уточните, пожалуйста, вас интересует? ")