# Файл по требованиям для зачета (get_price)
import telebot
from config import keys
from tok import TOKEN
from extensions import ApiExeption, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message: telebot.types.Message):
    bot.reply_to(message, "-Чтобы произвести обмен валют отправьте сообщение боту в виде <имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> через пробел \n-Наберите /start или /help чтобы ознакомиться с инструкцией. \n-Команда /values - позволит увидеть перечень доступных для обмена валют.")


@bot.message_handler(commands=["values"])
def handle_values(message: telebot.types.Message):
    text = "Доступны следующие валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ApiExeption("Количество параметров не соответсвует требуемому")
        base, quote, amount = values
        total_base = CriptoConverter.get_price(base, quote, amount)
    except ApiExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message.chat.id, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)
bot.polling()