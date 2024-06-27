from django.contrib import admin
from .models import Follow, Profile, Notification, Message

admin.site.register(Follow)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(Message)