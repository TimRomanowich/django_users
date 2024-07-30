from django.contrib import admin, messages
from django.urls import path
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, ChatPrivilege
from .views import manage_all_privileges_view

# Register your models here.
admin.site.register(Profile)

# admin.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ChatPrivilege, User

@admin.register(ChatPrivilege)
class ChatPrivilegeAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_post', 'can_read', 'can_post_media')
    actions = ['manage_privileges']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('manage-all-privileges/', self.admin_site.admin_view(manage_all_privileges_view), name='manage_all_privileges'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['manage_all_privileges_url'] = 'admin:manage_all_privileges'
        return super().changelist_view(request, extra_context=extra_context)
   
    def manage_privileges(self, request, queryset):
        if len(queryset) == 1:
            return redirect('admin:manage-privileges', user_id=queryset[0].user.id)
        self.message_user(request, "Please select only one user at a time to manage privileges.", level=messages.WARNING)
    manage_privileges.short_description = "Manage user privileges"

    def manage_privileges_view(self, request, user_id):
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