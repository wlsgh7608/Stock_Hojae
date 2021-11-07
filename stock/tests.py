from django.test import TestCase
from .models import UsStocklist
# Create your tests here.


class StockTest(TestCase):

    def test_check(self):
        self.assertEqual(1,1)