# backend/tasks.py


from django.core.mail import send_mail
from celery import shared_task

from backend.models import ConfirmEmailToken, User
from stonks import settings


# @shared_task(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
#     """
#     Отправляем письмо с токеном для сброса пароля
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param kwargs:
#     :return:
#     """
#     #send an e-mail to the user
#
#     msg = EmailMultiAlternatives(
#         # title:
#         f"Password Reset Token for {reset_password_token.user}",
#         # message:
#         reset_password_token.key,
#         # from:
#         settings.EMAIL_HOST_USER,
#         # to:
#         [reset_password_token.user.email]
#     )
#     msg.send()


@shared_task()
def new_user_registered(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    send_mail(
        f"Password Reset Token for {token.user.email}",
        token.key,
        settings.EMAIL_HOST_USER,
        [token.user.email],
        fail_silently=False,
        )


@shared_task()
def new_order(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    send_mail(
        "Обновление статуса заказа",
        "заказ сформирован",
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        )




