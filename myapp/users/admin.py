from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Specify all fields for display and editing
    fields = ('username', 'email', 'password', 'user_type', 'is_active', 'is_staff', 'is_superuser')

# Register the CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)
