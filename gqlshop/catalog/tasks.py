from django_rq import job
from catalog.models import CurrencyRate
import requests


@job('default')
def update_currency_rate():
    queryset = CurrencyRate.objects.all()
    for rate in queryset:
        pair = '{}RUB'.format(rate.currency.upper())
        response = requests.get(
            'https://www.freeforexapi.com/api/live?pairs={}'.format(pair)
        )
    data = response.json()

    rate.rate = data['rates'][pair]['rate']
    rate.save(update_fields=['rate'])
    return True
