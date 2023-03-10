# #import os
# # import pathlib
# # from pathlib import Path
# from distutils.util import strtobool
#
# from django.contrib.auth import authenticate
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
# from django.core.validators import URLValidator
# from django.db import IntegrityError
# from django.db.models import Q, Sum, F
# from django.http import JsonResponse
# from django.views.generic import CreateView
# from requests import get
# from rest_framework.authtoken.models import Token
# from rest_framework.generics import ListAPIView
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from json import loads as load_json
# from yaml import load as load_yaml, Loader
# from rest_framework.throttling import AnonRateThrottle
#
# from backend.models import  ConfirmEmailToken
# from backend.serializers import UserSerializer
# from django.http import HttpResponse, HttpResponseNotFound, Http404
# from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *

# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         ]


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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'backend/register.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Регистрация'
            }

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Регистрация'
    #      return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     c_def = self.get_user_context(title="Регистрация")
    #     return dict(list(context.items()) + list(c_def.items()))


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'backend/login.html'
    extra_context= {
        'title': 'Вход'
              }

    def get_success_url(self):
        return reverse_lazy('new_profile')


def logout_user(request):
    logout(request)
    return redirect('login')


class AddProfile(LoginRequiredMixin, CreateView):
    form_class = AddProfileForm
    template_name = 'backend/new_profile.html'
    success_url = reverse_lazy('*********home')
    login_url = reverse_lazy('***********home')
    raise_exception = True
    extra_context = {
        'title': 'AddProfile'
              }


class ShowProfile(DetailView):
    model = Profile
    template_name = 'backend/profile.html'
    allow_empty = False
    extra_context = {
        'title': 'Profile'
              }

    def get_queryset(self, prof_id):
        return Profile.objects.get(pk=prof_id)
    # def get_queryset(self, request, *args, **kwargs):
    #     id = args[0] # or id = kwargs['id'] if it is passed as keyword argument
    #     self.profile = get_object_or_404(Profile, id=pk, owner=request.user)
    #     return super(ShowProfile, self).dispatch(request, pk)
# def data_profile(request):
#     return HttpResponse("Данные профиля")


# def login(request):
#     return HttpResponse("Авторизация")
#
#
# def logout(request):
#     return HttpResponse("Вы вышли из авторизации")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
