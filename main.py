"""
Данный файл представляет Tg-бота https://t.me/DimIl_POPUTI_bot, который помогает
оставить заявку для бронирования номера в гостевом доме "ДимИль"
и магазине аксессуаров в дорогу "ПОПУТИ".
"""

import telebot
import messages
from peewee import *
from config import TOKEN

# Константы
BOT = telebot.TeleBot(TOKEN)
DATABASE_NAME = 'database_Dimil.db'
CLIENTS_INFO = {}

# База данных
DB = SqliteDatabase(DATABASE_NAME)


@BOT.message_handler(commands=["start"])
@BOT.message_handler(func=lambda message: message.text == messages.BUTTON_REVERSE)
def welcome(message: telebot.types.Message) -> None:
    """
    Отправляет приветственное сообщение.
    Показывает клавиатуру с двумя кнопками: ДимИль и ПОПУТИ.
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=messages.BUTTON_DIMIL)
    button2 = telebot.types.KeyboardButton(text=messages.BUTTON_POPUTI)
    keyboard.add(button1)
    keyboard.add(button2)
    BOT.send_message(
        chat_id,
        "Здравствуйте! Уточните пожалуйста, что вас интересует? ",
        reply_markup=keyboard
    )
    BOT.register_next_step_handler(message, answer)


def answer(message: telebot.types.Message) -> None:
    """
    Выбирает вопрос по теме:
    если "ДимИль", запускает процесс бронирования через client_name;
    если "ПОПУТИ", выводит информацию и переходит к choice_POPUTI.
    """
    chat_id = message.chat.id
    CLIENTS_INFO[chat_id] = {}
    if message.text == messages.BUTTON_DIMIL:
        BOT.send_message(chat_id, messages.BUTTON_BOOKING_GUEST_INFO)
        client_name(message)
    elif message.text == messages.BUTTON_POPUTI:
        BOT.send_message(chat_id, messages.BUTTON_INFO_POPUTI)
        choice_POPUTI(message)
    else:
        print('Неверный формат сообщения')


def choice_POPUTI(message: telebot.types.Message) -> None:
    """
    Выводит информацию о магазине ПОПУТИ.
    Отображает кнопки:
    контактная информация (BUTTON_CONTACT_POPUTI);
    вернуться назад (BUTTON_REVERSE).
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=messages.BUTTON_CONTACT_POPUTI)
    button2 = telebot.types.KeyboardButton(text=messages.BUTTON_REVERSE)
    keyboard.add(button1)
    keyboard.add(button2)
    BOT.send_message(chat_id, "Поступайте на курсы в Cursera", reply_markup=keyboard)
    BOT.register_next_step_handler(message, choice_answer_POPUTI)


def choice_answer_POPUTI(message: telebot.types.Message) -> None:
    """
    Выводит информацию о магазине ПОПУТИ.
    Отображает кнопки:
    контактная информация (BUTTON_CONTACT_POPUTI);
    вернуться назад (BUTTON_REVERSE).
    """
    chat_id = message.chat.id
    CLIENTS_INFO[chat_id] = {}
    if message.text == messages.BUTTON_CONTACT_POPUTI:
        BOT.send_message(chat_id, messages.MESSAGE_CONTACT_POPUTI)
        welcome(message)
    elif message.text == messages.BUTTON_REVERSE:
        welcome(message)
    else:
        print('Неверный формат сообщения')


def client_name(message: telebot.types.Message) -> None:
    """
    Запрашивает имя пользователя и переходит к сбору телефона через BUTTON_PHONE_NUMBER.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.CLIENT_NAME)
    CLIENTS_INFO[chat_id]['username'] = message.text
    BOT.register_next_step_handler(message, button_phone_number)


def button_phone_number(message: telebot.types.Message) -> None:
    """
    Запрашивает номер телефона пользователя и переходит к сбору даты через BUTTON_FLEXIBLE_DATE.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_PHONE_NUMBER)
    CLIENTS_INFO[chat_id]['phone_number'] = message.text
    BOT.register_next_step_handler(message, button_flexible_date)


def button_flexible_date(message: telebot.types.Message) -> None:
    """
    Запрашивает гибкую дату бронирования и переходит к сбору даты заезда через ANSWER_BUTTON_CHECK_IN.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_FLEXIBLE_DATE)
    CLIENTS_INFO[chat_id]['flexible_date'] = message.text
    BOT.register_next_step_handler(message, answer_button_check_in)


def answer_button_check_in(message: telebot.types.Message) -> None:
    """
    Запрашивает дату заезда и переходит к дате выезда через ANSWER_BUTTON_CHECK_OUT.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_CHECK_IN)
    CLIENTS_INFO[chat_id]['enter_date'] = message.text
    BOT.register_next_step_handler(message, answer_button_check_out)


def answer_button_check_out(message: telebot.types.Message) -> None:
    """
    Запрашивает дату выезда и переходит к количеству взрослых через ANSWER_BUTTON_ADULTS.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_CHECK_OUT)
    CLIENTS_INFO[chat_id]['out_date'] = message.text
    BOT.register_next_step_handler(message, answer_button_adults)


def answer_button_adults(message: telebot.types.Message) -> None:
    """
    Запрашивает количество взрослых и переходит к количеству детей через ANSWER_BUTTON_CHILDREN.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_ADULTS)
    CLIENTS_INFO[chat_id]['adult'] = message.text
    BOT.register_next_step_handler(message, answer_button_children)


def answer_button_children(message: telebot.types.Message) -> None:
    """
    Запрашивает количество детей и завершает процесс бронирования через add_client.
    """
    chat_id = message.chat.id
    BOT.send_message(chat_id, messages.BUTTON_CHILDREN)
    CLIENTS_INFO[chat_id]['children'] = message.text
    BOT.register_next_step_handler(message, add_client)


class TDIMIL(Model):
    """
    При запуске создается таблица TDIMIL.

    Поля:
    CLIENT_NAME: Имя клиента;
    BUTTON_PHONE_NUMBER: Номер телефона;
    BUTTON_FLEXIBLE_DATE: Гибкая дата бронирования;
    BUTTON_CHECK_IN: Дата заезда;
    BUTTON_CHECK_OUT: Дата выезда;
    BUTTON_ADULTS: Количество взрослых;
    BUTTON_CHILDREN: Количество детей.
    """
    client_name = CharField()
    button_phone_number = CharField()
    button_flexible_date = CharField()
    button_check_in = CharField()
    button_check_out = CharField()
    button_adults = CharField()
    button_children = CharField()

    class Meta:
        database = DB


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
    BOT.send_message(chat_id, messages.MESSAGE_ABOUT_DIMIL)
    choice(message)


def choice(message: telebot.types.Message) -> None:
    """
    Выводит главное меню с кнопками: ДимИль, ПОПУТИ, Назад.
    """
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = telebot.types.KeyboardButton(text=messages.BUTTON_REVERSE)
    button1 = telebot.types.KeyboardButton(text=messages.BUTTON_DIMIL)
    button2 = telebot.types.KeyboardButton(text=messages.BUTTON_POPUTI)
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    BOT.send_message(
        chat_id,
        "Нефритовый жезл ",
        reply_markup=keyboard
    )


if __name__ == "__main__":
    print("Бот запущен!")
    BOT.infinity_polling()
