"""
Модуль с взаимодействием с базой данных Tg-бота https://t.me/DimIl_POPUTI_bot, который помогает
оставить заявку для бронирования номера в гостевом доме "ДимИль"
и магазине аксессуаров в дорогу "ПОПУТИ".
"""
from peewee import *

# Настройка базы данных
DATABASE_NAME = 'database_Dimil.db'
DB = SqliteDatabase(DATABASE_NAME)


class TDIMIL(Model):
    """
    Модель для таблицы TDIMIL.

    Поля:
    - client_name: Имя клиента;
    - button_phone_number: Номер телефона;
    - button_flexible_date: Гибкая дата бронирования;
    - button_check_in: Дата заезда;
    - button_check_out: Дата выезда;
    - button_adults: Количество взрослых;
    - button_children: Количество детей.
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


def initialize_database():
    """
    Инициализирует базу данных и создает таблицы, если их нет.
    """
    DB.connect()
    DB.create_tables([TDIMIL], safe=True)
