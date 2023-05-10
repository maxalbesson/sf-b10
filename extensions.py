import requests
import json
from config import currency, headers


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_currency(base, quote, amount):
        try:
            base_value = currency[base]
        except KeyError:
            raise APIException(f'Неверное имя валюты: "{base}".')
        try:
            quote_value = currency[quote]
        except KeyError:
            raise APIException(f'Неверное имя валюты: "{quote}".')
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не указано число: "{amount}".')

        if currency[quote] == currency[base]:
            raise APIException('Введены одинаковые валюты.')

        url = f'https://api.apilayer.com/exchangerates_data/latest?base={base_value}&symbols={quote_value}'
        response = requests.get(url, headers=headers)
        result = json.loads(response.content)
        total = result['rates'][quote_value] * amount
        return total
