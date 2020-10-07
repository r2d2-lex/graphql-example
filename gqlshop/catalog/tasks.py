from django_rq import job
from .models import CurrencyRate
import requests


def get_currency_rate(currency):
    pair = '{}RUB'.format(currency.upper())
    response = requests.get(
        'https://www.freeforexapi.com/api/live?pairs={}'.format(pair)
    )
    data = response.json()
    return data['rates'][pair]['rate']


@job('default')
def update_currency_rate():
    queryset = CurrencyRate.objects.all()
    for rate in queryset:
        rate.rate = get_currency_rate(rate.currency)
        rate.save(update_fields=['rate'])
    return True
