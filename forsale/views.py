from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Categories

# TODO for development
is_signed_in = False

# Add colours:
#
# highlight_bg_color: background for divisions, headings.
#     Indicates signed in status.
#
def add_colors(request, context):
    if is_signed_in:
        highlight_bg_color = "#FFA07A" # LightSalmon
    else:
        highlight_bg_color = "#90EE90" # LightGreen
    context["highlight_bg_color"] = highlight_bg_color


def index(request):
    return categories(request)


def categories(request):
    categories_list = Categories.objects.order_by("name")

    context = {
        "categories_list": categories_list,
    }
    add_colors(request, context)

    return render(request, "forsale/categories.html", context)

