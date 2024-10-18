import telebot
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
    CLIENTS_INFO[chat_id] = {}
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
    bot.register_next_step_handler(message, add_client)


db = SqliteDatabase('database_Dimil.db')

class TDIMIL(Model):
    client_name = CharField()
    button_phone_number = CharField()
    button_flexible_date = CharField()
    button_check_in = CharField()
    button_check_out = CharField()
    button_adults = CharField()
    button_children = CharField()

    class Meta:
        database = db

TDIMIL.create_table()

def add_client(message: telebot.types.Message):
    chat_id = message.chat.id
    new_client = TDIMIL(
        client_name='Philipp', #username,
        button_phone_number= 890909099999, #phone_number,
        button_check_in=CLIENTS_INFO[chat_id]["enter_date"],
        button_check_out=CLIENTS_INFO[chat_id]["out_date"],
        button_flexible_date='yes', #flexible_date,
        button_adults=CLIENTS_INFO[chat_id]["adult"],
        button_children=CLIENTS_INFO[chat_id]["children"]
    )
    new_client.save()
    bot.send_message(chat_id, messages.message_about_DimIL)

if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()


#@bot.message_handler(func=lambda message: message.text == "Здравствуйте! Уточните, пожалуйста, вас интересует? ")