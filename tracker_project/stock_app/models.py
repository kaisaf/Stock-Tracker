from django.db import models
from django.contrib.auth.models import User
from stock_scraper.models import Stock
import requests
import json

# Create your models here.
class UserStock(models.Model):
    user = models.ForeignKey(User)
    stock = models.ForeignKey(Stock)
    variation = models.FloatField()
    minutes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PERCENT = 'PCT'
    PRICE = 'PR'
    VOLUME = 'VOL'
    STD = 'STD'
    VARIATION_TYPE_CHOICES = (
        (PERCENT, 'Percent'),
        (PRICE, 'Price'),
        (VOLUME, 'Volume'),
        (STD, 'Standard Deviation'),
    )
    variation_type = models.CharField(max_length=3, choices=VARIATION_TYPE_CHOICES)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.id, self.user, self.stock, self.variation_type, self.variation)

    def check_alert(self, user_stock):
        data = user_stock.stock.get_intraday_data()
        if not data:
            return None
        sliced_data = data[len(data)-user_stock.minutes:]
        price_change_pct, price_change_dol = self.calculate_variations(sliced_data)
        if user_stock.variation_type == "PCT":
            return self.variation < price_change_pct
        elif user_stock.variation_type == "PR":
            return self.variation < price_change_dol

    def calculate_variations(self, data):
        newest = data[-1]
        oldest = data[0]
        price_change_pct = abs(((newest["close"] - oldest["close"])/oldest["close"]) * 100)
        price_change_dol = abs(newest["close"] - oldest["close"])
        return price_change_pct, price_change_dol
