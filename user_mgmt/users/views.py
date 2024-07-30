from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View

from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, user_passes_test

from django.http import JsonResponse

from django.urls import reverse
from rest_framework import generics, permissions, status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .middleware import get_online_users
from .forms import RegisterForm, LoginForm
from .models import Profile, ChatPrivilege
from .serializers import UserRegistrationSerializer, ProfileSerializer, DeleteUserSerializer, LoginSerializer, ChatPrivilegeSerializer

# Create your views here.
def home(request):
    return render(request, 'users/home.html')
def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def manage_privileges_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    chat_privilege, created = ChatPrivilege.objects.get_or_create(user=user)

    if request.method == 'POST':
        can_post = 'can_post' in request.POST
        can_read = 'can_read' in request.POST
        can_post_media = 'can_post_media' in request.POST

        chat_privilege.update_privileges(can_post=can_post, can_read=can_read, can_post_media=can_post_media)
        messages.success(request, f"Privileges updated for {user.username}")
        return redirect('admin:users_chatprivilege_changelist')

    context = {
        'title': f"Manage Privileges for {user.username}",
        'chat_privilege': chat_privilege,
    }
    return render(request, 'admin/manage_privileges.html', context)

@user_passes_test(is_admin)
def update_user_privilege(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        chat_privilege, created = ChatPrivilege.objects.get_or_create(user=user)
        chat_privilege.can_post = 'can_post' in request.POST
        chat_privilege.can_read = 'can_read' in request.POST
        chat_privilege.can_post_media = 'can_post_media' in request.POST
        chat_privilege.save()
    return redirect('manage_all_privileges')

@user_passes_test(is_admin)
def manage_all_privileges_view(request):
    users = User.objects.all()
    chat_privileges = ChatPrivilege.objects.all()
    user_privileges = {cp.user_id: cp for cp in chat_privileges}
    
    context = {
        'users': users,
        'user_privileges': user_privileges,
    }
    return render(request, 'admin/manage_privs.html', context)
class DeleteUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DeleteUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            # Logout the user
            logout(request)
            # Delete the user
            user.delete()
            return Response({"detail": "User account has been successfully deleted."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EditProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        serializer.save()
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({'message': 'Please send a POST request to login'})
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

    def get(self, request):
        return Response({'message': 'Click the POST button to logout'})
    
"""
#Login View using JWT 
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
"""
#Logout view using JWT
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
"""
            
"""
# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
"""
        
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
def online_users_api(request):
    online_users = get_online_users()
    data = [{'username': user.username, 'last_activity': user.last_activity} for user in online_users]
    return JsonResponse(data, safe=False)

def online_users_list(request):
    online_users = get_online_users()
    return render(request, 'users/online_users.html', {'online_users': online_users})

def all_users_api(request):
    users = User.objects.all()
    data = [{
        'username': user.username,
        'email': user.email,
        'profile_url': request.build_absolute_uri(reverse('users-profile', kwargs={'username': user.username}))
    } for user in users]
    return JsonResponse(data, safe=False)

class ChatPrivilegeViewSet(viewsets.ModelViewSet):
    queryset = ChatPrivilege.objects.all()
    serializer_class = ChatPrivilegeSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserChatPrivilegeView(generics.RetrieveUpdateAPIView):
    serializer_class = ChatPrivilegeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return ChatPrivilege.objects.get_or_create(user=self.request.user)[0]
    
# Limits access to logged in users
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'profile_user': user})



