import os.path

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from .models import Categories

# Add common context for views:
#
# origin_url_name: The name of this url path.
#
# user.username: User name if user is logged in.
#
# highlight_bg_color: background for divisions, headings.
#     Indicates signed in status.
#
# signinout_bg_color: The opposite colour of highlight_bg_color.
#
# debug: Optional debug message, must be added to the template to see it.
#
def add_context(request, context):
    # I couldn't find an easier way to get the original page name, so
    # use last element of the path. Ensure they are the same in urls.py.
    context["origin_url_name"] = os.path.basename(request.path)

    if request.user.is_authenticated:
        highlight_bg_color = "#FFD700" # Gold
        signinout_bg_color = "#90EE90" # LightGreen

        context["user.username"] = request.user.username
    else:
        highlight_bg_color = "#90EE90" # LightGreen
        signinout_bg_color = "#FFD700" # Gold
    context["highlight_bg_color"] = highlight_bg_color
    context["signinout_bg_color"] = signinout_bg_color
# debug
#    context["debug"] = "debug message"


def index(request):
    return categories(request)


def categories(request):
    categories_list = Categories.objects.order_by("name")

    context = {
        "categories_list": categories_list,
    }
    add_context(request, context)

    return render(request, "forsale/categories.html", context)


def signin(request, origin_url_name):
    context = { }
    add_context(request, context)

    return render(request, "forsale/signin.html", context)


def signin_done(request, origin_url_name):
    context = { }
    add_context(request, context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        context["signin_error"] = "user is not None"  # debug
        login(request, user)
        return HttpResponseRedirect(reverse(f"forsale:{origin_url_name}"))
    else:
        # No backend authenticated the credentials
        context['signin_error'] = "Username or password incorrect"
        return render(request, "forsale/signin.html", context)

def signout_done(request, origin_url_name):
    # Logout and return to original page.
    logout(request)

    context = { }
    add_context(request, context)

    return HttpResponseRedirect(reverse(f"forsale:{origin_url_name}"))

