import telebot
from config import token, currency
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Введите 3 значения через пробел в следующем формате:\n<имя рассчетной валюты> <имя интересующей валюты> ' \
           '<количество рассчетной валюты>;\nсписок доступных валют: /values.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for curr in currency.keys():
        text = '\n'.join((text, curr))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split()
        total = CurrencyConverter.get_currency(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка работы бота.\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Критическая ошибка.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total}'
        bot.send_message(message.chat.id, text)


bot.polling()
