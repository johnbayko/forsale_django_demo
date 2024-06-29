import os.path

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
    return HttpResponseRedirect(reverse(f"forsale:categories"))


def categories(request):
    categories_list = Categories.objects.order_by("name")

    context = {
        "categories_list": categories_list,
    }
    add_context(request, context)

    return render(request, "forsale/categories.html", context)


def items(request, category_id):





    items_list = Items.objects.order_by("created")

    context = {
        "items_list": items_list,
    }
    add_context(request, context)

    return render(request, "forsale/items.html", context)


def signin(request, origin_url_name):
    context = { }
    add_context(request, context)

    return render(request, "forsale/signin.html", context)


def signin_done(request, origin_url_name):
    context = { }
    add_context(request, context)

    missing_values = [ ]

    username = request.POST['username']
    context['username'] = username
    if username == '':
        missing_values.append("Username")

    password = request.POST['password']
    if password == '':
        missing_values.append("Password")

    if len(missing_values) > 0:
        context['signin_error'] = \
            "These values are needed to continue: " + ", ".join(missing_values)
        return render(request, "forsale/signin.html", context)

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse(f"forsale:{origin_url_name}"))
    else:
        # No backend authenticated the credentials
        try:
            User.objects.get(username=username)
            context['signin_error'] = "Password is incorrect"
        except User.DoesNotExist:
            context['signin_error'] = f"No user found with username: {username}"

        return render(request, "forsale/signin.html", context)

def signout_done(request, origin_url_name):
    # Logout and return to original page.
    logout(request)

    context = { }
    add_context(request, context)

    return HttpResponseRedirect(reverse(f"forsale:{origin_url_name}"))


def signup(request, origin_url_name):
    context = {
        "username": request.POST['username'],
        "password": request.POST['password'],
    }
    add_context(request, context)

    return render(request, "forsale/signup.html", context)


def signup_done(request, origin_url_name):
    context = { }
    add_context(request, context)

    missing_values = [ ]

    username = request.POST['username']
    context['username'] = username
    if username == '':
        missing_values.append("Username")

    password = request.POST['password']
    context['password'] = password
    if password == '':
        missing_values.append("Password")

    password2 = request.POST['password2']
    context['password2'] = password2
    if password2 == '':
        missing_values.append("Retype password")

    first_name = request.POST['first_name']
    context['first_name'] = first_name

    last_name = request.POST['last_name']
    context['last_name'] = last_name

    email = request.POST['email']
    context['email'] = email
    if email == '':
        missing_values.append("Email")

    if len(missing_values) > 0:
        context['signup_error'] = \
            "These values are needed to continue: " + ", ".join(missing_values)
        return render(request, "forsale/signup.html", context)

    if password != password2:
        context['signup_error'] = "Password wasn't the same both times,"
        return render(request, "forsale/signup.html", context)

    # Add a new user.
    try:
        newuser = User.objects.create_user(username, password=password, email=email)
        # Add user info record.
        newuserinfo = Userinfo.objects.create(user=newuser, username=username)
        newuserinfo.save()

    except IntegrityError:
        context['signup_error'] = f"User {username} already exists."
        return render(request, "forsale/signup.html", context)
    except ValueError:
        context['signup_error'] = f"Username {username} isn't valid."
        return render(request, "forsale/signup.html", context)

    newuser_changed = False
    if first_name != "":
        newuser.first_name = first_name
        newuser_changed = True
    if last_name != "":
        newuser.last_name = last_name
        newuser_changed = True
    if newuser_changed:
        newuser.save()

    # Log in new user.
    login(request, newuser)
    return HttpResponseRedirect(reverse(f"forsale:{origin_url_name}"))

