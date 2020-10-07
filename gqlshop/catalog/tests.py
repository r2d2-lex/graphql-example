from django.test import TestCase
from .models import CurrencyRate
from .tasks import get_currency_rate, update_currency_rate
import mock


class FakeResponse:
    def json(self):
        return {
            "rates":
                {
                    "USDRUB":
                        {
                            "rate": 60.5,
                            "timestamp": 1602076146
                        }
                },
            "code": 200
        }


class CurrencyRateTestCase(TestCase):
    @mock.patch('requests.get', return_value=FakeResponse())
    def test_get_currency_rate(self, mocked_get):
        rate = get_currency_rate('usd')
        self.assertEqual(rate, 60.5, 'Rate value not equal to 60.5')
        self.assertTrue(mocked_get.called)

    @mock.patch('requests.get', return_value=FakeResponse())
    def test_update_currency_rate(self, mocked_get):
        rate = CurrencyRate.objects.create(currency='usd')
        self.assertEqual(rate.rate, 1)

        self.assertTrue(update_currency_rate())
        rate = CurrencyRate.objects.get(currency='usd')
        self.assertEqual(rate.rate, 60.5, 'Rate value not equal to 60.5')

# Example Mock 1
# class CurrencyRateTestCase(TestCase):
#
#     def test_get_currency_rate(self):
#         with mock.patch('requests.get', return_value=FakeResponse()):
#             rate = get_currency_rate('usd')
#             self.assertEqual(rate, 60.5, 'Rate value not equal to 60.5')
