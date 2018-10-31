from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'apps.account'

    # def ready(self):
    #     import apps.account.registration.checks  # noqa
    #     import apps.account.signals  # noqa
