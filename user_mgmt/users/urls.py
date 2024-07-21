from django.urls import path
from .views import home, RegisterView, profile, online_users_api, online_users_list, all_users_api, RegisterUserAPIView

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('online-list/', online_users_list, name='online-users-list'),
    path('api/online/', online_users_api, name='online-users-api'),
    path('api/users/', all_users_api, name='all-users-api'),
    path('api/register/', RegisterUserAPIView.as_view(), name='register-api'),
]
