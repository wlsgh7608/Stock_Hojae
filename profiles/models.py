# from django.db import models
# from django.contrib.auth.models import UserManager,AbstractUser
# # Create your models here.


# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.utils import timezone
# from django.utils.translation import ugettext_lazy as _


# class UserManager(BaseUserManager):
#     use_in_migrations = True
#     def _create_user(self, email, password):
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None):
#         return self._create_user(email, password)


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     customized User
#     """
#     email = models.EmailField(
#         verbose_name=_('email id'),
#         max_length=64,
#         unique=True,
#         help_text='EMAIL ID.'
#     )
#     username = models.CharField(
#         max_length=30,
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#     objects = UserManager()

#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def __str__(self):
#         return self.username

#     def get_short_name(self):
#         return self.email
    
