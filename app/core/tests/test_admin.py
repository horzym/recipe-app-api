from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdminSite(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='testadmin@site.com',
            password='testadminsite123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='emial@test.com',
            password='test123',
            name='Test Name'
        )

    def test_user_listed(self):
        """Test if user are listed in admin site"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user change site works, if works status page equal 200"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add(self):
        """Test add user in admin page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
