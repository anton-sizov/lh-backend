from django.urls import reverse
from rest_framework import status

from apps.common.testing import BaseTestCase # pylint: disable=no-name-in-module
# from .models import LHUser


class AccountTest(BaseTestCase):
    api_url = '/api/v1/'
    use_test_account = True

    def test_registration(self):
        url = reverse('account-register')

        email = 'new_user@test.ru'
        data = {
            'email': email,
            'password': 'pass54321',
            'password_confirm': 'pass54321'
        }
        response = self.post(url, data, expected_status=status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('email'), email)

    def test_registration_fail(self):
        url = reverse('account-register')

        # test non-matching passwords
        email = 'new_user@test.ru'
        data = {
            'email': email,
            'password': 'pass54321',
            'password_confirm': 'random'
        }
        self.post(url, data, expected_status=status.HTTP_400_BAD_REQUEST)

        # test non-unique email
        data = {
            'email': 'test@test.ru',
            'password': 'pass54321',
            'password_confirm': 'pass54321'
        }
        self.post(url, data, expected_status=status.HTTP_400_BAD_REQUEST)
