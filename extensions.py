import requests
from config import keys
import lxml.html


class APIException(Exception):
    pass
class API:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'В запросе указанны одинаковые валюты-{base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту, обратите внимание валюты вводятся с маленькой буквы - {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')


        r = requests.get(f'https://currconv.ru/{amount}-{base_ticker}-to-{quote_ticker}').content
        tree = lxml.html.document_fromstring(r)
        total_base = tree.xpath('/html/body/div[1]/div/article/div[1]/h2/span[1]/text()')
        total_base = total_base[0].replace(' ', '')
        return total_base