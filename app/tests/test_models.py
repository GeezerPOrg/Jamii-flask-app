import unittest
from app.models.models import User, Businesses
from werkzeug.security import check_password_hash, generate_password_hash

class TestModel(unittest.TestCase):
    def setUp(self):
        self.user = User()
        self.business = Businesses()

    def test_user_instance(self):
        victor = User()
        self.assertIsInstance(victor, User)

    def test_business_instance(self):
        motorhub = Businesses()
        self.assertIsInstance(motorhub, Businesses)

    def test_user_object_type(self):
        desagu = User()
        self.assertTrue(type(desagu) is User)

    def test_business_object_type(self):
        motorhub = Businesses()
        self.assertTrue(type(motorhub) is Businesses)

    # def test_check_password_method(self):
    #     result = self.user.check_password(check_password_hash(self.user.set_password('mypassword'),'mypassword'))
    #     self.assertEqual(result, True)
