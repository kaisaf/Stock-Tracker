from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, "stock_app/index.html")

class HomeView(View):
    def get(self, request):
        return render(request, "stock_app/home.html")

class SignUpView(View):
    def get(self, request):
        return render(request, "stock_app/signup.html")

class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated():
            print("already logged in and going home")
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
