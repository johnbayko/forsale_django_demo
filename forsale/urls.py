from django.urls import path

from . import views

app_name = "forsale"
urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("signin/<slug:origin_url_name>", views.signin, name="signin"),
    path("signin_done/<slug:origin_url_name>", views.signin_done, name="signin_done"),
    path("signout_done/<slug:origin_url_name>", views.signout_done, name="signout_done"),
    path("signup/<slug:origin_url_name>", views.signup, name="signup"),
    path("signup_done/<slug:origin_url_name>", views.signup_done, name="signup_done"),
]
