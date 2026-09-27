from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, Account, Card, Transaction

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Transaction)