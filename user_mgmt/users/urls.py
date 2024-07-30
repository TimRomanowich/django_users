from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (home, RegisterView, profile, online_users_api, 
                    online_users_list, all_users_api, RegisterUserAPIView, 
                    EditProfileAPIView, DeleteUserAPIView, LoginView, LogoutView,
                    ChatPrivilegeViewSet, UserChatPrivilegeView, manage_privileges_view, manage_all_privileges_view, update_user_privilege)
router = DefaultRouter()
router.register(r'chat-privileges', ChatPrivilegeViewSet)

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
     path('api/', include(router.urls)),
    path('api/my-chat-privileges/', UserChatPrivilegeView.as_view(), name='my-chat-privileges'),
    path('admin/manage-privileges/<int:user_id>/', manage_privileges_view, name='manage-privileges'),
    path('admin/manage-privileges/', manage_all_privileges_view, name='manage_all_privileges'),
    path('admin/update-privilege/<int:user_id>/', update_user_privilege, name='update_user_privilege'),
]
