"""
Данный файл представляет Tg-бота https://t.me/DimIl_POPUTI_bot, который помогает
оставить заявку для бронирования номера в гостевом доме "ДимИль"
и магазине аксессуаров в дорогу "ПОПУТИ".
"""

import telebot
import messages
from peewee import *
from config import TOKEN
bot = telebot.TeleBot(TOKEN)


#CLIENTS_INFO - словарь в котором находятся промежуточные пользовательские данные
CLIENTS_INFO = {

}

@bot.message_handler(commands=["start"])
@bot.message_handler(func = lambda message: message.text == messages.button_reverse)
def welcome(message: telebot.types.Message) -> None:
    """
    Отправляет приветственное сообщение.
    Показывает клавиатуру с двумя кнопками: ДимИль и ПОПУТИ.
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=messages.button_DimIl)
    button2 = telebot.types.KeyboardButton(text=messages.button_POPUTI)
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(
        chat_id,
        "Здравствуйте! Уточните пожалуйста, что вас интересует? ",
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, answer)


def answer(message: telebot.types.Message) -> None:
    """
    Выбирает вопрос по теме:
    если "ДимИль", запускает процесс бронирования через client_name;
    если "ПОПУТИ", выводит информацию и переходит к choice_POPUTI.
    """

    chat_id = message.chat.id
    CLIENTS_INFO[chat_id] = {}
    if message.text == messages.button_DimIl:
        bot.send_message(chat_id, messages.button_booking_guest_info)
        client_name(message)
    elif message.text == messages.button_POPUTI:
        bot.send_message(chat_id, messages.button_info_POPUTI)
        choice_POPUTI(message)
    else:
        print('Неверный формат сообщения')

def choice_POPUTI(message: telebot.types.Message) -> None:
    """
    Выводит информацию о магазине ПОПУТИ.
    Отображает кнопки:
    контактная информация (button_contact_POPUTI);
    вернуться назад (button_reverse).
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=messages.button_contact_POPUTI)
    button2 = telebot.types.KeyboardButton(text=messages.button_reverse)
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(chat_id, "Поступайте на курсы в Cursera", reply_markup=keyboard)
    bot.register_next_step_handler(message, choice_answer_POPUTI)

def choice_answer_POPUTI(message: telebot.types.Message) -> None:
    """
    Выводит информацию о магазине ПОПУТИ.
    Отображает кнопки:
    контактная информация (button_contact_POPUTI);
    вернуться назад (button_reverse).
    """
    chat_id = message.chat.id
    CLIENTS_INFO[chat_id] = {}
    if message.text == messages.button_contact_POPUTI:
        bot.send_message(chat_id, messages.message_contact_POPUTI)
        welcome(message)
    elif message.text == messages.button_reverse:
        welcome(message)
    else:
        print('Неверный формат сообщения')


def client_name(message: telebot.types.Message) -> None:
    """
    Запрашивает имя пользователя и переходит к сбору телефона через button_phone_number.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.client_name)
    CLIENTS_INFO[chat_id]['username'] = message.text
    bot.register_next_step_handler(message, button_phone_number)

def button_phone_number(message: telebot.types.Message) -> None:
    """
    Запрашивает номер телефона пользователя и переходит к сбору даты через button_flexible_date.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_phone_number)
    CLIENTS_INFO[chat_id]['phone_number'] = message.text
    bot.register_next_step_handler(message, button_flexible_date)

def button_flexible_date(message: telebot.types.Message) -> None:
    """
    Запрашивает гибкую дату бронирования и переходит к сбору даты заезда через answer_button_check_in.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_flexible_date)
    CLIENTS_INFO[chat_id]['flexible_date'] = message.text
    bot.register_next_step_handler(message, answer_button_check_in)

def answer_button_check_in(message: telebot.types.Message) -> None:
    """
    Запрашивает дату заезда и переходит к дате выезда через answer_button_check_out.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_check_in)
    CLIENTS_INFO[chat_id]['enter_date'] = message.text
    bot.register_next_step_handler(message, answer_button_check_out)

def answer_button_check_out(message: telebot.types.Message) -> None:
    """
    Запрашивает дату выезда и переходит к количеству взрослых через answer_button_adults.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_check_out)
    CLIENTS_INFO[chat_id]['out_date'] = message.text
    print(message.text)
    bot.register_next_step_handler(message, answer_button_adults)

def answer_button_adults(message: telebot.types.Message) -> None:
    """
    Запрашивает количество взрослых и переходит к количеству детей через answer_button_children.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_adults)
    CLIENTS_INFO[chat_id]['adult'] = message.text
    print(message.text)
    bot.register_next_step_handler(message, answer_button_children)

def answer_button_children(message: telebot.types.Message) -> None:
    """
    Запрашивает количество детей и завершает процесс бронирования через add_client.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.button_children)
    CLIENTS_INFO[chat_id]['children'] = message.text
    print(message.text)
    bot.register_next_step_handler(message, add_client)

#База данных
db = SqliteDatabase('database_Dimil.db')


class TDIMIL(Model):
    """
    При запуске создается таблица TDIMIL.

    Поля:
    client_name: Имя клиента;
    button_phone_number: Номер телефона;
    button_flexible_date: Гибкая дата бронирования;
    button_check_in: Дата заезда;
    button_check_out: Дата выезда;
    button_adults: Количество взрослых;
    button_children: Количество детей.
    """
    client_name = CharField()
    button_phone_number = CharField()
    button_flexible_date = CharField()
    button_check_in = CharField()
    button_check_out = CharField()
    button_adults = CharField()
    button_children = CharField()

    class Meta:
        database = db

"""
База данных
"""
TDIMIL.create_table()

def add_client(message: telebot.types.Message) -> None:
    """
    Сохраняет данные пользователя в базу данных.
    Отправляет сообщение об успешном бронировании.
    Возвращает пользователя к выбору действия через choice.
    """
    chat_id = message.chat.id
    new_client = TDIMIL(
        client_name=CLIENTS_INFO[chat_id]['username'],
        button_phone_number=CLIENTS_INFO[chat_id]['phone_number'],
        button_check_in=CLIENTS_INFO[chat_id]["enter_date"],
        button_check_out=CLIENTS_INFO[chat_id]["out_date"],
        button_flexible_date=CLIENTS_INFO[chat_id]['flexible_date'],
        button_adults=CLIENTS_INFO[chat_id]["adult"],
        button_children=CLIENTS_INFO[chat_id]["children"]
    )
    new_client.save()
    bot.send_message(chat_id, messages.message_about_DimIL)
    choice(message)


def choice(message: telebot.types.Message) -> None:
    """
    Выводит главное меню с кнопками: ДимИль, ПОПУТИ, Назад.
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = telebot.types.KeyboardButton(text=messages.button_reverse)
    button1 = telebot.types.KeyboardButton(text=messages.button_DimIl)
    button2 = telebot.types.KeyboardButton(text=messages.button_POPUTI)
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    bot.send_message(
        chat_id,
        "Нефритовый жезл ",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
