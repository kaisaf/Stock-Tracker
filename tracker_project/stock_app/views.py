from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserStock
import matplotlib.pyplot as plt


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect("home")
        return render(request, "stock_app/index.html")

class HomeView(View):
    def get(self, request):
        context = {"username": request.user.username}
        stocks = UserStock.objects.filter(user=request.user)
        stocks_table = []
        symbols = []
        fig = plt.figure()
        for stock in stocks:
            stock_data = stock.get_info()
            if not stock_data:
                continue
            plt.plot(stock_data["prices"])
            symbols.append(stock.symbol)
            tmp = {
                "id": stock.id,
                "symbol": stock.symbol,
                "variation_type": stock.variation_type,
                "variation": stock.variation,
                "alerts": stock_data["alerts"]
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
        new_stock = UserStock(user=request.user, symbol=frm_symbol, variation=frm_variation, variation_type=frm_variation_type)
        if not new_stock.get_min_by_min_data():
            messages.add_message(request, messages.ERROR, 'Symbol not valid')
        else:
            new_stock.save()
        return redirect("home")

class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect("home")
        return render(request, "stock_app/signup.html")

    def post(self, request):
        frm_username = request.POST["username"]
        frm_email = request.POST["email"]
        frm_password = request.POST["password"]
        if frm_username == "" or frm_password == "":
            context = {"error_message": "Username and Password are mandatory fields"}
            return render(request, "stock_app/signup.html", context)
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
        if user:
            login(request, user)
            return redirect("home")
        else:
            context = {"error_message": "Wrong username or password"}
            return render(request, "stock_app/signin.html", context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
