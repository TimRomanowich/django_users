from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            request.user.last_activity = now
            request.user.save()
        response = self.get_response(request)
        return response

def get_online_users():
    # Consider users active in the last 5 minutes as online
    time_threshold = timezone.now() - timezone.timedelta(minutes=5)
    return User.objects.filter(last_activity__gte=time_threshold)