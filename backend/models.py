
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.tokens import get_token_generator

from .managers import UserManager

# STATE_CHOICES = (
#     ('basket', 'Статус корзины'),
#     ('new', 'Новый'),
#     ('confirmed', 'Подтвержден'),
#     ('assembled', 'Собран'),
#     ('sent', 'Отправлен'),
#     ('delivered', 'Доставлен'),
#     ('canceled', 'Отменен'),
# )



# class BaseModel(models.Model):
#     objects = models.Manager()
#
#     class Meta:
#         abstract = True


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(_('name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('email',)

    def get_short_name(self):
        '''
        Returns the  name for the user.
        '''
        return self.name








 # class Contact(BaseModel):
#     user = models.ForeignKey(User, verbose_name='Пользователь',
#                              related_name='contacts', blank=True,
#                              on_delete=models.CASCADE)
#
#     city = models.CharField(max_length=50, verbose_name='Город')
#     street = models.CharField(max_length=100, verbose_name='Улица')
#     house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
#     structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
#     building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
#     apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#
#     class Meta:
#         verbose_name = 'Контакты пользователя'
#         verbose_name_plural = "Список контактов пользователя"
#
#     def __str__(self):
#         return f'{self.city} {self.street} {self.house}'



class ConfirmEmailToken(models.Model):

    objects = None   # это возможно нужно убрать, по совету от IDE

    class Meta:
        verbose_name = 'Токен подтверждения Email'
        verbose_name_plural = 'Токены подтверждения Email'

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return get_token_generator().generate_token()

    user = models.ForeignKey(
        User,
        related_name='confirm_email_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("The User which is associated to this password reset token")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("When was this token generated")
    )

    # Key field, though it is not the primary key of the model
    key = models.CharField(
        _("Key"),
        max_length=64,
        db_index=True,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ConfirmEmailToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)
