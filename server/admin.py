from django.contrib import admin

from .models import User, UserNote

# Register your models here.

class AdminView(admin.ModelAdmin):
  list_display = ['id', 'email', 'is_admin', 'is_superuser', 'date_created']

admin.site.register(User, AdminView)

class UserNoteView(admin.ModelAdmin):
  list_display = ['user', 'title', 'date_created']

admin.site.register(UserNote, UserNoteView)