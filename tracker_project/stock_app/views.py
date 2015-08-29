from django.shortcuts import render
from django.views.generic import View

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
        return render(request, "stock_app/signin.html")
