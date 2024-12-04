"""
Модуль содержит клавиатуры, используемые в телеграм-боте https://t.me/DimIl_POPUTI_bot, который помогает
оставить заявку для бронирования номера в гостевом доме "ДимИль"
и магазине аксессуаров в дорогу "ПОПУТИ".
"""

import telebot
from telebot import types
import messages

class KeyboardBot:
    """
    Класс содержит основные клавиатуры, используемые в боте.
    """

    @staticmethod
    def main_menu() -> telebot.types.ReplyKeyboardMarkup:
        """
        Главное меню с кнопками: ДимИль, ПОПУТИ.
        """
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text=messages.BUTTON_DIMIL)
        button2 = telebot.types.KeyboardButton(text=messages.BUTTON_POPUTI)
        keyboard.add(button1)
        keyboard.add(button2)
        return keyboard

    @staticmethod
    def shop_menu() -> telebot.types.ReplyKeyboardMarkup:
        """
        Меню магазина ПОПУТИ с кнопками:
        - Контактная информация;
        - Назад.
        """
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text=messages.BUTTON_CONTACT_POPUTI)
        button2 = telebot.types.KeyboardButton(text=messages.BUTTON_REVERSE)
        keyboard.add(button1)
        keyboard.add(button2)
        return keyboard

    @staticmethod
    def extended_menu() -> telebot.types.ReplyKeyboardMarkup:
        """
        Расширенное меню с кнопками: ДимИль, ПОПУТИ, Назад.
        """
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button3 = telebot.types.KeyboardButton(text=messages.BUTTON_REVERSE)
        button1 = telebot.types.KeyboardButton(text=messages.BUTTON_DIMIL)
        button2 = telebot.types.KeyboardButton(text=messages.BUTTON_POPUTI)
        keyboard.add(button1)
        keyboard.add(button2)
        keyboard.add(button3)
        return keyboard
