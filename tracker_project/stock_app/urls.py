"""tracker_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from .views import HomeView, IndexView, SignUpView, SignInView, LogoutView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^home/$', login_required(HomeView.as_view()), name='home'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signin/$', SignInView.as_view(), name='signin'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^home/delete/$', csrf_exempt(DeleteView.as_view()), name='delete'),

]
