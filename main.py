import telebot

from config import TOKEN
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message: telebot.types.Message) -> None:
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text=" Гостевой дом «ДимИль»")
    button2 = telebot.types.KeyboardButton(text=" Аксессуары в дорогу «ПОПУТИ»")
    keyboard.add(button1)
    keyboard.add(button2)
    bot.send_message(
        chat_id,
        "Здравствуйте! Уточните, пожалуйста, вас интересует? ",
        reply_markup=keyboard
    )

def answer(message: telebot.types.Message) -> None:
    chat_id = message.chat.id

    if message.text not in messages.keys() and message.text != "Начать тестирование":


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()


#@bot.message_handler(func=lambda message: message.text == "Здравствуйте! Уточните, пожалуйста, вас интересует? ")