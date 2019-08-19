from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_superuser_acc(self):
        """Test create superuser account"""
        user = get_user_model().objects.create_superuser(
            'admin@admin.com',
            'rootpassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_new_user_without_emial(self):
        """check if new user want to register but dont pass emial address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'passwordtest123')

    def test_new_user_email_normalized(self):
        """check if email is normalized"""
        email = 'test@UnNorMaliZedEmail.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_create_user_with_emial_succesful(self):
        """test creat user with emial"""
        email = 'testemial"emial.com'
        password = 'passwordtest'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
