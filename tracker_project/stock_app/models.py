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
        return "{} - {} - {} - {}".format(self.user, self.stock, self.variation_type, self.variation)
