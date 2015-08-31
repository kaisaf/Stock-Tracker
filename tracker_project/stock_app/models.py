from django.db import models
from django.contrib.auth.models import User
import requests
import json

# Create your models here.
class UserStock(models.Model):
    user = models.ForeignKey(User)
    symbol = models.CharField(max_length=10)
    variation = models.FloatField()
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
        return "{} - {} - {} - {}".format(self.user, self.symbol, self.variation_type, self.variation)

    def get_info(self):
        data = self.get_min_by_min_data()
        if not data:
            return None
        price_list = self.get_price_list(data)
        sliced_data = data[len(data)-10:]
        variations = self.check_alert(sliced_data)
        stock_data = {
            "alerts": variations,
            "prices": price_list
        }
        return stock_data

    def check_alert(self, sliced_data):
        variations = self.calculate_variations(sliced_data)
        if self.variation < variations[self.variation_type]:
            return variations
        return None

    def get_min_by_min_data(self):
        url = "http://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=2d/json".format(self.symbol)
        server_answer = requests.get(url)
        if "errorid" in server_answer.text:
            return None
        else:
            data = server_answer.text[server_answer.text.index('(')+1:]
            data = data[:-2]
            data = json.loads(data)
            data = data["series"]
            return data

    def get_price_list(self, data):
        price_list = []
        for item in data:
            price = item["close"]
            price_list.append(price)
        return price_list


    def calculate_variations(self, data):
        newest = data[-1]
        oldest = data[0]
        price_change_pct = (newest["close"] - oldest["close"])/oldest["close"]
        price_change_dol = newest["close"] - oldest["close"]
        vol_change = newest["volume"] - oldest["volume"]
        variations = {
            "PCT":price_change_pct,
            "PR": price_change_dol,
            "VOL": vol_change
            }
        return variations
