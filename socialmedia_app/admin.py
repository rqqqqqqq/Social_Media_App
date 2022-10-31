from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# add post to admin
admin.site.register(Post)

class AccountAdmin(UserAdmin):
    # define whic fields are shown in django admin
    list_display = ('user_email','username','date_joined', 'last_login', 'is_admin','is_staff')
    # fields used for searching in django admin
    search_fields = ('user_email','username',)
    # information on each user is added
    readonly_fields=('id', 'date_joined', 'last_login')

    # remove filter section
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user',]

    class Meta:
        model = FriendList

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver',]
    # search fields used in admin page search bar
    search_fields = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendRequest



admin.site.register(Account, AccountAdmin)
admin.site.register(FriendList, FriendListAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)