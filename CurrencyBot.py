import telebot
from Config import currencies, TOKEN
from classes import ConvertionException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start","help"])
def greeting(message: telebot.types.Message):
    text = ("Приветствую, для того, чтобы начать работу, отправьте мне команду в следующем формате: \n<Название валюты, из которой надо перевести> \
<Название валюты, в которую надо перевести> \
<Количесвто переводимой валюты>\n\nПример: Евро Рубль 10\n\nНазвания валют обязательно вводить в единственном числе и с заглавной буквы \
\n\nЧтобы увидеть список доступных валют, введите следующую команду: /values\n\nДля повторного просмотра этой инструкции введите /help")
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def value(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in currencies.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler(content_types=["text"],)
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Неверное количество параметров\nЕсли у вас возникли проблемы, введите /help")

        base, quote, amount = values
        total_base = CurrencyConverter.converter(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя. \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        amount = float(amount)
        total_base = total_base * amount
        text = f"Цена {amount} {base} в {quote} - {total_base}"
        bot.send_message(message.chat.id, text)











bot.polling(non_stop=True)


