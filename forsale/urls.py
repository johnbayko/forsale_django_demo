from django.urls import path

from . import views

app_name = "forsale"
urlpatterns = [
    path("", views.index, name="index"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>/items/", views.categoryitems, name="categoryitems"),
    path("user/<int:user_id>/items/", views.useritems, name="useritems"),
    path("user/<int:user_id>/newitem/", views.newitem, name="newitem"),
    path("user/<int:user_id>/newitem_done/", views.newitem_done, name="newitem_done"),

    path("item/<int:item_id>/", views.item, name="item"),
    path("item/<int:item_id>/remove/", views.itemremove, name="itemremove"),
    path("item/<int:item_id>/bid/", views.itembid, name="itembid"),
    path("item/<int:item_id>/withdraw/", views.itemwithdraw, name="itemwithdraw"),
    path("item/<int:item_id>/offer/<int:offer_id>/accept/", views.offeraccept, name="offeraccept"),
    path("item/<int:item_id>/offer/<int:offer_id>/unaccept/", views.offerunaccept, name="offerunaccept"),
    path("item/<int:item_id>/offer/<int:offer_id>/delivered/", views.offerdelivered, name="offerdelivered"),

    path("user/<path:origin_path>/", views.user, name="user"),
    path("user_done/<path:origin_path>/", views.user_done, name="user_done"),

    path("signin/<path:origin_path>/", views.signin, name="signin"),
    path("signin_done/<path:origin_path>/", views.signin_done, name="signin_done"),
    path("signout_done/<path:origin_path>/", views.signout_done, name="signout_done"),
    path("signup/<path:origin_path>/", views.signup, name="signup"),
    path("signup_done/<path:origin_path>/", views.signup_done, name="signup_done"),
]
