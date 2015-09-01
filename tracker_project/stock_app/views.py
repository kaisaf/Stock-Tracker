from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserStock
from stock_scraper.models import Stock
import matplotlib.pyplot as plt
import yahoo_finance


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect("home")
        return render(request, "stock_app/index.html")

class HomeView(View):
    def get(self, request):
        context = {"username": request.user.username}
        user_stocks = UserStock.objects.filter(user=request.user)
        stocks_table = []
        symbols = []
        fig = plt.figure()
        for user_stock in user_stocks:
#            stock_data = Stock.objects.get(id=user_stock.stock)
            plt.plot(user_stock.stock.get_price_list())
            symbols.append(user_stock.stock.symbol)
            alert = user_stock.stock.check_alert(user_stock.variation_type, user_stock.variation)

            tmp = {
                "id": user_stock.stock.id,
                "symbol": user_stock.stock.symbol,
                "variation_type": user_stock.variation_type,
                "variation": user_stock.variation,
                "alert": alert
            }
            stocks_table.append(tmp)
        context["stocks"] = stocks_table
        filename = "stock_app/static/stock_app/images/{}".format(request.user.username)
        plt.legend(symbols)
        fig.savefig(filename)
        return render(request, "stock_app/home.html", context)

    def post(self, request):
        frm_symbol = request.POST["symbol"]
        frm_variation_type = request.POST["variation_type"]
        frm_variation = request.POST["variation"]
        frm_minutes = request.POST["minutes"]
#        if self.validate_stock_symbol(frm_symbol):
        stock = Stock.objects.filter(symbol=frm_symbol).first()
        if not stock:
            stock = Stock(symbol=frm_symbol)
            stock.refresh_yahoo_api_data()
            stock.refresh_yahoo_intraday_data()
            stock.refresh_plot()
            stock.save()
        new_stock = UserStock(user=request.user, stock=stock, variation=frm_variation, variation_type=frm_variation_type, minutes=frm_minutes)
        new_stock.save()
#        else:
#            messages.add_message(request, messages.ERROR, 'Symbol not valid')
        return redirect("home")

    def validate_stock_symbol(self, symbol):
        share = yahoo_finance.Share(symbol)
        if len(share.get_info()) > 1:
            return True
        return False

class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect("home")
        return render(request, "stock_app/signup.html")

    def post(self, request):
        frm_username = request.POST["username"]
        # if User.objects.get(username=frm_username):
        #     context = {"error_message": "Username must be unique"}
        #     return render(request, "stock_app/signup.html", context)
        frm_email = request.POST["email"]
        frm_password = request.POST["password"]
        user = User.objects.create_user(username=frm_username, email=frm_email, password=frm_password)
        user = authenticate(username=frm_username, password=frm_password)
        login(request, user)
        return redirect("home")

class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect("home")
        return render(request, "stock_app/signin.html")

    def post(self, request):
        frm_username = request.POST["username"]
        frm_password = request.POST["password"]
        user = authenticate(username=frm_username, password=frm_password)
        login(request, user)
        return redirect("home")

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
