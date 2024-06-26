from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Categories

# Add colours:
#
# highlight_bg_color: background for divisions, headings.
#     Indicates signed in status.
#
def add_colors(request, context):

    if request.user.is_authenticated:
        highlight_bg_color = "#FFA07A" # LightSalmon
        signinout_bg_color = "#90EE90" # LightGreen

        context["user.username"] = request.user.username
    else:
        highlight_bg_color = "#90EE90" # LightGreen
        signinout_bg_color = "#FFA07A" # LightSalmon
    context["highlight_bg_color"] = highlight_bg_color
    context["signinout_bg_color"] = signinout_bg_color
#    context["debug"] = "username:" + request.user.username


def index(request):
    return categories(request)


def categories(request):
    categories_list = Categories.objects.order_by("name")

    context = {
        "categories_list": categories_list,
    }
    add_colors(request, context)

    return render(request, "forsale/categories.html", context)

