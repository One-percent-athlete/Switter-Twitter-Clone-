from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Swit
# Register your models here.

admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username",'first_name', 'last_name','is_superuser']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Swit)

