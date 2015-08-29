from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserStock

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "stock_app/index.html")

class HomeView(View):
    def get(self, request):
        context = {"username": request.user.username}
        stocks = UserStock.objects.filter(user=request.user)
        context["stocks"] = stocks
        return render(request, "stock_app/home.html", context)
    def post(self, request):
        frm_symbol = request.POST["symbol"]
        frm_variation_type = request.POST["variation_type"]
        frm_variation = request.POST["variation"]
        new_stock = UserStock(user=request.user, symbol=frm_symbol, variation=frm_variation, variation_type=frm_variation_type)
        new_stock.save()
        print(new_stock)
        return redirect("home")

class SignUpView(View):
    def get(self, request):
        if request.user.is_authenticated():
            print("cant signup again and going home")
            return redirect("home")
        return render(request, "stock_app/signup.html")
    def post(self, request):
        print(request.POST)
        frm_username = request.POST["username"]
        frm_email = request.POST["email"]
        frm_password = request.POST["password"]
        user = User.objects.create_user(username=frm_username, email=frm_email, password=frm_password)
        user = authenticate(username=frm_username, password=frm_password)
        login(request, user)
        return redirect("home")

class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated():
            print("cant sign in again and going home")
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
        print("logging out")
        logout(request)
        return redirect("index")
