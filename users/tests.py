"""My boilerplate custom user tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


SAMPLE_EMAIL, SAMPLE_PW = 'random@random.net', 'foo'


class UsersManagersTests(TestCase):

    def setUp(self) -> None:
        self.user_model = get_user_model()

    def test_create_user(self):
        user = self.user_model.objects.create_user(email=SAMPLE_EMAIL, password=SAMPLE_PW, is_active=False)

        self.assertTrue(check_password(SAMPLE_PW, user.password))
        self.assertIsNone(user.last_login)
        self.assertFalse(user.is_superuser)

        # Customized:
        self.assertEqual(user.email, SAMPLE_EMAIL)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)

        with self.assertRaises(TypeError):
            self.user_model.objects.create_user()
        with self.assertRaises(TypeError):
            self.user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(email='', password=SAMPLE_PW)

    def test_create_superuser(self):
        admin_user = self.user_model.objects.create_superuser(SAMPLE_EMAIL, SAMPLE_PW)

        self.assertTrue(check_password(SAMPLE_PW, admin_user.password))
        self.assertIsNone(admin_user.last_login)
        self.assertTrue(admin_user.is_superuser)

        # Customized:
        self.assertEqual(admin_user.email, SAMPLE_EMAIL)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)

        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(email=SAMPLE_EMAIL, password=SAMPLE_PW, is_superuser=False)
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(email=SAMPLE_EMAIL, password=SAMPLE_PW, is_staff=False)
