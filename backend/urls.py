

from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from backend.views import login, logout, data_profile, start, RegisterUser


app_name = 'backend'
urlpatterns = [
     path('', start, name='home'),
     path('login/', login, name='login'),
     path('logout/', logout, name='logout'),
     path('register/', RegisterUser.as_view(), name='register'),
     path('profile/', data_profile, name='profile'),
]

     # path('user/password_reset/', reset_password_request_token, name='password-reset'),
     # path('user/password_reset/confirm/', reset_password_confirm, name='password-reset-confirm'),
     # path('user/register/', RegisterAccount.as_view(), name='user-register'),
     # path('user/register/confirm/', ConfirmAccount.as_view(), name='user-register-confirm'),
     # path('user/details/', AccountDetails.as_view(), name='user-details'),
     # path('user/login/', LoginAccount.as_view(), name='user-login'),
     # #path('user/contact/', ContactView.as_view(), name='user-contact'),  # работа с контактами пок-лей GET POST PUT DEL


