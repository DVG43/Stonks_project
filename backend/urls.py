

from django.urls import path
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

from backend.views import start, RegisterUser, LoginUser, logout_user, AddProfile, ShowProfile


app_name = 'backend'
urlpatterns = [
     path('', start, name='home'),
     path('login/', LoginUser.as_view(), name='login'),
     path('logout/', logout_user, name='logout'),
     path('register/', RegisterUser.as_view(), name='register'),
     path('profile/<int:prof_id>/', ShowProfile.as_view(), name='profile'),
     path('new_profile/', AddProfile.as_view(), name='new_profile'),
]

     # path('user/password_reset/', reset_password_request_token, name='password-reset'),
     # path('user/password_reset/confirm/', reset_password_confirm, name='password-reset-confirm'),
     # path('user/register/', RegisterAccount.as_view(), name='user-register'),
     # path('user/register/confirm/', ConfirmAccount.as_view(), name='user-register-confirm'),
     # path('user/details/', AccountDetails.as_view(), name='user-details'),
     # path('user/login/', LoginAccount.as_view(), name='user-login'),
     # #path('user/contact/', ContactView.as_view(), name='user-contact'),  # работа с контактами пок-лей GET POST PUT DEL


