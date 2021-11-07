from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
# Create your tests here.

from pybo.models import Blog, Comment
from stock.models import UsStocklist
User = get_user_model()


class PyboTestCase(TestCase):

    def setUp(self):
        aapl = UsStocklist.objects.create(symbol = 'AAPL',name = 'aaple',industry = 'asdf',industry_id = 1234)
        msft = UsStocklist.objects.create(symbol = 'MSFT',name = 'microsoft',industry = 'asdf',industry_id = 1234)
        stock = UsStocklist.objects.get(symbol = 'AAPL')
        self.user1 = User.objects.create_user(username = 'testcase1',password = '1234')
        self.user2 = User.objects.create_user(username = 'testcase2',password = '1234')
        Blog.objects.create(title ='my title test1',body = 'my body test1',symbol = stock,user = self.user1)
        Blog.objects.create(title ='my title test2',body = 'my body test2',symbol = stock,user = self.user2)
        self.currentCount = Blog.objects.all().count()

    def test_check_ok(self):
        self.assertEqual(1,1)

    def test_blog_create(self):
        blog_obj = Blog.objects.create(title = 'create test',body = 'body create test', symbol =self.stock, user = self.user1)
        self.assertEqual(blog_obj.id,3)





