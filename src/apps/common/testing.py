import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class BaseTestCase(APITestCase):
    api_url = ''
    use_test_account = True
    test_user_data = {
        'email': 'test@test.ru',
        'password': 'pass54321'
    }
    test_account = None

    @classmethod
    def setUpClass(cls):
        settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/test')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def setUp(self):
        super(BaseTestCase, self).setUp()
        if self.use_test_account and self.test_account is None:
            self.test_account = self.create_test_account()

    def send(self, command, parameters=None, method=None, auth_token=None, expected_status=status.HTTP_200_OK,
             check_error_code=True, **kwargs):

        parameters = parameters or []
        # if auth_token:
        #     self.client.credentials(HTTP_AUTHORIZATION='JWT' + auth_token)

        send_func = getattr(self.client, method, None)
        if send_func is None:
            raise BaseException('Incorrect method')
        response = send_func(command, data=parameters, **kwargs)

        if check_error_code:
            self.assertEqual(response.status_code, expected_status)

        return response

    def post(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
             check_error_code=True, **kwargs):
        return self.send(command, parameters, 'post', auth_token, expected_status, check_error_code, **kwargs)

    def get(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
            check_error_code=True, **kwargs):
        return self.send(command, parameters, 'get', auth_token, expected_status, check_error_code, **kwargs)

    def delete(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
               check_error_code=True, **kwargs):
        return self.send(command, parameters, 'delete', auth_token, expected_status, check_error_code, **kwargs)

    def patch(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
              check_error_code=True, **kwargs):
        return self.send(command, parameters, 'patch', auth_token, expected_status, check_error_code, **kwargs)

    def put(self, command, parameters=None, auth_token=None, expected_status=status.HTTP_200_OK,
            check_error_code=True, **kwargs):
        return self.send(command, parameters, 'put', auth_token, expected_status, check_error_code, **kwargs)

    def make_api_url(self, url):
        return os.path.join(self.api_url, url)

    def account_create(self, email, password, **kwargs):
        user = User(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def account_create_and_login(self, email, password, **kwargs):
        self.account_create(email, password, **kwargs)
        return self.get_api_token(email, password)

    def get_api_token(self, email, password, expected_status=status.HTTP_200_OK):
        url = reverse('account-login')

        data = {'email': email, 'password': password}

        response = self.client.post(url, data, format='json')
        token = response.data.get('token')

        self.assertEqual(response.status_code, expected_status)

        return token

    def create_test_account(self):
        return self.account_create(**self.test_user_data)

    def get_test_account_token(self, expected_status=status.HTTP_200_OK):
        return self.get_api_token(self.test_user_data['email'], self.test_user_data['password'], expected_status)
