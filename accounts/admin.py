from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

#if you want changaable profile in admin page
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date', 'created_at')
    search_fields = ("user__username", "phone")
    list_filter = ("birth_date", )

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
