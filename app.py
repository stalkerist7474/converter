import telebot
from config import keys, TOKEN
from extensions import APIException,API


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Обработчик комманд старт и помощь
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите соответствующую команду боту в следующем формате: \n<Имя валюты> \
    <В какую валюту перевести> \
    <Количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)  # бот отвечает на ваше сообщение команды


@bot.message_handler(commands=['values'])  # Обработчик комманд асортимента валют
def values(message: telebot.types.Message):
    text = 'Доступные типы валют:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # Обработчик текста
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise APIException('Слишком много параметров в запросе.')

        quote, base, amount = value
        total_base = API.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base} {keys[quote]}'
        bot.send_message(message.chat.id, text)  # бот отвечает




bot.polling()