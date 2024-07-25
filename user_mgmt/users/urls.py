from django.urls import path
from .views import (home, RegisterView, profile, online_users_api, 
                    online_users_list, all_users_api, RegisterUserAPIView, 
                    EditProfileAPIView, DeleteUserAPIView, LoginView, LogoutView)
urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/<str:username>/', profile, name='users-profile'),
    path('online-list/', online_users_list, name='online-users-list'),
    path('api/online/', online_users_api, name='online-users-api'),
    path('api/users/', all_users_api, name='all-users-api'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/register/', RegisterUserAPIView.as_view(), name='register-api'),
    path('api/profile/edit/', EditProfileAPIView.as_view(), name='edit-profile-api'),
    path('api/account/delete/', DeleteUserAPIView.as_view(), name='delete-account-api'),
]
