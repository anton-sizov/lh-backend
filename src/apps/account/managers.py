from django.contrib.auth.models import BaseUserManager


class LHUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=False, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
