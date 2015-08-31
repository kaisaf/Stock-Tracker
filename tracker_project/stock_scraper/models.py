from django.db import models

import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

from yahoo_finance import Share


class Stock(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    fifty_moving_avg = models.FloatField()
    two_hundred_moving_avg = models.FloatField()
    year_high = models.FloatField()
    year_low = models.FloatField()
    price_change_pct = models.FloatField()
    price_change_dol = models.FloatField()
    twenty_four_hours_price_list = models.TextField()
    last_ploted_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{} - 50days avg: {} - price change: {} - percent_change: {}".format(self.symbol, self.fifty_moving_avg, self.price_change_dol, self.price_change_pct)
    
    def refresh(self):
        """ Refresh instance data with if it is older than 60 seconds """
        if (datetime.now() - self.updated_at()) > 60:
            self.refresh_yahoo_api_data()
            self.refresh_yahoo_intraday_data()
    
    def refresh_plot(self):
        """ This method should be called by the view to update the graphic ploted if self.last_ploted_at
            passed a given time.
            This method should NOT be called by the server's service running every minute,
            we do not want waste resources ploting graphics no one is seeing.
        """
        fdir = "/stock_scraper/static/stock_scraper/tpm/imgs/"
        fig = plt.figure()
        plt.plot(self.get_price_list())
        plt.legend(self.symbol)
        plt.savefig("{}{}".format(fdir, self.symbol))
        self.last_ploted_at = datetime.now()
    
    def refresh_yahoo_api_data(self):
        yahoo_data = Share(self.symbol)
        self.fifty_moving_avg = yahoo_data.get_50day_moving_avg()
        self.two_hundred_moving_avg = yahoo_data.get_200day_moving_avg()
        self.year_high = yahoo_data.get_year_high()
        self.year_low = yahoo_data.get_year_low()
    
    def refresh_yahoo_intraday_data(self):
        intraday = self.get_intraday_data()
        self.twenty_four_hours_price_list = self.refresh_price_list(intraday)
        self.calculate_variations(intraday)
        
    
    def get_intraday_data(self):
        url = "http://chartapi.finance.yahoo.com/instrument/1.0/{}/chartdata;type=quote;range=1d/json".format(self.symbol)
        server_answer = requests.get(url)
        data = server_answer.text[server_answer.text.index('(')+1:]
        data = data[:-2]
        data = json.loads(data)
        data = data["series"]
        return data
    
    def refresh_price_list(self, data):
        price_list = ""
        for item in data:
            price = item["close"]
            price_list += str(price)
        return price_list
    
    def get_price_list(self):
        price_list = []
        price_str = self.twenty_four_hours_price_list.split(',')
        for price in price_str:
            price_list.append(float(price))
        return price_list
    
    def calculate_variations(self, data):
        newest = data[-1]
        oldest = data[0]
        self.price_change_pct = ((newest["close"] - oldest["close"])/oldest["close"]) * 100
        self.price_change_dol = newest["close"] - oldest["close"]
    