from django.contrib import admin
from .models import UserStock


class UserStockAdmin(admin.ModelAdmin):
    list_display = ('user', 'stock', 'variation', 'minutes', 'created_at')

admin.site.register(UserStock, UserStockAdmin)
