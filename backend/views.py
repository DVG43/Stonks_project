#import os
# import pathlib
# from pathlib import Path
from distutils.util import strtobool

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from requests import get
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from json import loads as load_json
from yaml import load as load_yaml, Loader
from rest_framework.throttling import AnonRateThrottle

from backend.models import  ConfirmEmailToken
from backend.serializers import UserSerializer
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from backend.task import new_user_registered, new_order


class RegisterAccount(APIView):
    """
    Для регистрации покупателей
    """
    # Регистрация методом POST
    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'name', 'email', 'password', }.issubset(request.data):
            errors = {}

            # проверяем пароль на сложность

            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                # проверяем данные для уникальности имени пользователя
                request.data._mutable = True
                request.data.update({})
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    # сохраняем пользователя
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    new_user_registered.send(sender=self.__class__, user_id=user.id)
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """
    # Регистрация методом POST
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):

            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetails(APIView):
    """
    Класс для работы данными пользователя
    """
    throttle_classes = [AnonRateThrottle]
    # получить данные
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # Редактирование методом POST
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        # проверяем обязательные аргументы

        if 'password' in request.data:
            errors = {}
            # проверяем пароль на сложность
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                # noinspection PyTypeChecker
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])

        # проверяем остальные данные
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})


class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """
    # Авторизация методом POST
    def post(self, request, *args, **kwargs):

        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])

            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)

                    return JsonResponse({'Status': True, 'Token': token.key})

            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


# class ContactView(APIView):
#     """
#     Класс для работы с контактами покупателей
#     """
#     throttle_classes = [AnonRateThrottle]
#
#     # получить мои контакты
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#         contact = Contact.objects.filter(
#             user_id=request.user.id)
#         serializer = ContactSerializer(contact, many=True)
#         return Response(serializer.data)
#
#     # добавить новый контакт
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#
#         if {'city', 'street', 'phone'}.issubset(request.data):
#             request.data._mutable = True
#             request.data.update({'user': request.user.id})
#             serializer = ContactSerializer(data=request.data)
#
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse({'Status': True})
#             else:
#                 JsonResponse({'Status': False, 'Errors': serializer.errors})
#
#         return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
#
#     # удалить контакт
#     def delete(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#
#         items_sting = request.data.get('items')
#         if items_sting:
#             items_list = items_sting.split(',')
#             query = Q()
#             objects_deleted = False
#             for contact_id in items_list:
#                 if contact_id.isdigit():
#                     query = query | Q(user_id=request.user.id, id=contact_id)
#                     objects_deleted = True
#
#             if objects_deleted:
#                 deleted_count = Contact.objects.filter(query).delete()[0]
#                 return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
#         return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
#
#     # редактировать контакт
#     def put(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
#
#         if 'id' in request.data:
#             if request.data['id'].isdigit():
#                 contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
#                 print(contact)
#                 if contact:
#                     serializer = ContactSerializer(contact, data=request.data, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                         return JsonResponse({'Status': True})
#                     else:
#                         JsonResponse({'Status': False, 'Errors': serializer.errors})
#
#         return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
#
def start(request):
    return render(request, 'backend/start_page.html')

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


