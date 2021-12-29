from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView

from django.urls import path
from .views import add_post, delete_post, loginfun, register_user, showdashboard, update_post



app_name = "account"
urlpatterns = [
    path('login/', loginfun, name = "login"),
    path('logout/', LogoutView.as_view(), name = "logout"), 
    path('signup/', register_user, name = "signup"),
    path('dashboard/', showdashboard, name = "dash"),
    path('dashboard/addpost', add_post, name = "addpost"),
    path('dashboard/updatepost/<slug:slug>', update_post, name = "updatepost"),
    path('dashboard/deletepost/<slug:slug>', delete_post, name = "deletepost"),

    

]