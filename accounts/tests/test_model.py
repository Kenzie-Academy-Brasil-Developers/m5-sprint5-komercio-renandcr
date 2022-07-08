from django.db import IntegrityError
from django.test import TestCase
from accounts.models import User

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = "henry@gmail.com"
        cls.first_name = "Tierry"
        cls.last_name = "Henry"
        cls.is_seller = True
        cls.password = "123456"

        cls.user = User.objects.create(
            email = cls.email,
            first_name = cls.first_name,
            last_name = cls.last_name,
            is_seller = cls.is_seller,
            password = cls.password
        )

    def test_unique_email_restriction(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email = self.email,
                first_name = self.first_name,
                last_name = self.last_name,
                is_seller = self.is_seller,
                password = self.password
            )

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_user_has_all_fields(self):
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)
        self.assertEqual(self.user.is_seller, self.is_seller)
        







