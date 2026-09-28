from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Account, Card, Transaction


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("phone_number",)
    list_display = ("phone_number", "is_staff", "is_superuser",)
    search_fields = ( "phone_number",)


admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Transaction)