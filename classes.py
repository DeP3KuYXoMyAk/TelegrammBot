import json
import requests
from Config import currencies


class ConvertionException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def converter(base: str, quote: str, amount: str):

        if base == quote:
            raise ConvertionException(
                f"Невозможно перевести {base} в {base}\nЕсли у вас возникли проблемы, введите /help")

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}\nЕсли у вас возникли проблемы, введите /help")

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}\nЕсли у вас возникли проблемы, введите /help")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количесвто {amount}\nЕсли у вас возникли проблемы, введите /help")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_base = json.loads(r.content)[currencies[quote]]

        return total_base