from django.contrib import admin
from .models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'created_at', 'updated_at')

admin.site.register(Stock, StockAdmin)
