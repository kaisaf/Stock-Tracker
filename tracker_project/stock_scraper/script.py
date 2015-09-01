import sys
import os
import json

import django

from twilio.rest import TwilioRestClient


sys.path.append('/Users/vmenezes/byteAcademy/Stock-Tracker/tracker_project/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tracker_project.settings")

django.setup()

from django.contrib.auth.models import User

from stock_scraper.models import Stock
from stock_app.models import UserStock



print("UPDATING STOCK INFO...")
stocks = Stock.objects.all()
for stock in stocks:
    stock.refresh_yahoo_api_data()
    stock.refresh_yahoo_intraday_data()
print("DONE UPDATING INFO!")


# TWILIO'S CONFIG
with open('twilio_settings.json') as data_file:
    twilio_settings = json.load(data_file)
account_sid = twilio_settings["account_sid"]
auth_token  = twilio_settings["auth_token"]
client = TwilioRestClient(account_sid, auth_token)


print("CHEKING ALERTS AND SENDING NEEDED MESSAGES...")
users = User.objects.all()
for user in users:
    user_stocks = UserStock.objects.filter(user=user)
    alerts = []
    for user_stock in user_stocks:
        if user_stock.stock.check_alert(user_stock.variation_type, user_stock.variation):
            alerts.append(user_stock.stock.symbol)
    if alerts:
        sms_txt = "You have notifications for {}".format(alerts)
        message = client.messages.create(body=sms_txt,
            to="+13474255413",    # Replace with your phone number
            from_="+14155992671") # Replace with your Twilio number



