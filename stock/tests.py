from django.test import TestCase
from .models import UsStocklist
from rest_framework.test import APIClient
# Create your tests here.


class StockTest(TestCase):

    def setUp(self):
        self.aapl = UsStocklist.objects.create(symbol = 'AAPL',name = 'aaple',industry = 'asdf',industry_id = 1234)
        self.msft = UsStocklist.objects.create(symbol = 'MSFT',name = 'microsoft',industry = 'asdf',industry_id = 1234)

    

    def test_current_number(self):
        self.assertEqual(UsStocklist.objects.all().count(),2)

    def test_check(self):
        self.assertEqual(1,1)