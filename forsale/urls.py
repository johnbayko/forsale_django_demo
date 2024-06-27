from django.urls import path

from . import views

app_name = "forsale"
urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("signin", views.signin, name="signin"),
    path("signin_done", views.signin_done, name="signin_done"),
]
