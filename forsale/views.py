import os.path

from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms.ForsaleForms import NewItemForm
from .models import Categories, Items, Userinfo

# Add common context for views:
#
# origin_path: The name of this path.
#
# user_username: User name if user is logged in.
#
# highlight_bg_color: background for divisions, headings.
#     Indicates signed in status.
#
# signinout_bg_color: The opposite colour of highlight_bg_color.
#
# debug: Optional debug message, must be added to the template to see it.
#
def add_context(request, context):
    # I couldn't find an easier way to get return to the original page, so
    # add the current path to context, and add that as a parameter when linking
    # to pages that need to return.
    if "origin_path" not in context:
        context["origin_path"] = request.path

    if request.user.is_authenticated:
        highlight_bg_color = "#FFD700" # Gold
        signinout_bg_color = "#90EE90" # LightGreen

        context["user_username"] = request.user.username

        namelist = []
        if request.user.first_name != '':
            namelist.append(request.user.first_name)

        if request.user.last_name != '':
            namelist.append(request.user.last_name)

        if len(namelist) == 0:
            # No actual name, use username.
            namelist.append(request.user.username)

        context["user_fullname"] = " ".join(namelist)

    else:
        highlight_bg_color = "#90EE90" # LightGreen
        signinout_bg_color = "#FFD700" # Gold
    context["highlight_bg_color"] = highlight_bg_color
    context["signinout_bg_color"] = signinout_bg_color
# debug
#    context["debug"] = context["origin_path"]


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
    category = Categories.objects.get(pk=category_id)
    context = {
        "category": category,
    }

    refreshed_view = "refreshed_view" in request.GET

    if not refreshed_view:
        # First view, use defaults
        show_user_only = False
        show_sold = True
        show_removed = True
    else:
        show_user_only = "show_user_only" in request.GET
        show_sold = "show_sold" in request.GET
        show_removed = "show_removed" in request.GET

    if show_user_only:
        print('show_user_only')  # debug
        context["show_user_only"] = "show_user_only"
    if show_sold:
        print('show_sold')  # debug
        context["show_sold"] = "show_sold"
    if show_removed:
        print('show_removed')  # debug
        context["show_removed"] = "show_removed"

    if request.user.is_authenticated:
        user = request.user
        userinfo = Userinfo.objects.get(user=user)

        owner_items_list = \
            Items.objects \
                .filter(owner=userinfo, category=category)
        if not show_sold:
            owner_items_list = owner_items_list.filter(sold=False)
        if not show_removed:
            owner_items_list = owner_items_list.filter(removed=False)

        if show_user_only:
            items_list = owner_items_list
        else:
            # Add in non-owner items, but only not sold or removed.
            non_owner_items_list = \
                Items.objects \
                    .exclude(owner=userinfo)\
                    .filter(category=category, sold=False, removed=False)
            items_list = owner_items_list.union(non_owner_items_list)
    else:
        items_list = \
            Items.objects \
                .filter(category=category, sold=False, removed=False)
    context["items_list"] = items_list

    add_context(request, context)

    return render(request, "forsale/items.html", context)


def useritems(request, user_id):
    if not request.user.is_authenticated:
        # Apparently signed out while looking at this.
        return HttpResponseRedirect(reverse(f"forsale:categories"))

    user = request.user
    userinfo = Userinfo.objects.get(user=user)

    context = {
        "user": user
    }

    refreshed_view = "refreshed_view" in request.GET

    if not refreshed_view:
        # First view, use defaults
        show_sold = True
        show_removed = True
    else:
        show_sold = "show_sold" in request.GET
        show_removed = "show_removed" in request.GET

    if show_sold:
        print('show_sold')  # debug
        context["show_sold"] = "show_sold"
    if show_removed:
        print('show_removed')  # debug
        context["show_removed"] = "show_removed"

    items_list = Items.objects.filter(owner=userinfo)
    if not show_sold:
        items_list = items_list.filter(sold=False)
    if not show_removed:
        items_list = items_list.filter(removed=False)
    context["items_list"] = items_list

    add_context(request, context)

    return render(request, "forsale/useritems.html", context)


def newitem(request, user_id):
    if not request.user.is_authenticated:
        # Apparently signed out while looking at this.
        return HttpResponseRedirect(reverse(f"forsale:categories"))

    user = request.user
    userinfo = Userinfo.objects.get(user=user)

    context = {
        "user": user,
        "newitemform": NewItemForm(),
    }
    add_context(request, context)

    return render(request, "forsale/newitem.html", context)


def newitem_done(request, user_id):
    if not request.user.is_authenticated:
        # Apparently signed out while looking at this.
        return HttpResponseRedirect(reverse(f"forsale:categories"))

    user = request.user
    userinfo = Userinfo.objects.get(user=user)

    context = {
        "user": user
    }

    newitemform = NewItemForm(request.POST)
    context["newitemform"] = newitemform

    if not newitemform.is_valid():
        # TODO add error messaging
        return render(request, "forsale/newitem.html", context)

    # Actually add the item.
    newitem = Items.objects.create(
        owner = userinfo,
        category = newitemform.cleaned_data['category'],
        description = newitemform.cleaned_data['description'],
        price = int(newitemform.cleaned_data['price'] * 100),
        sold = False,
        removed = False
    )
    return HttpResponseRedirect(reverse(f"forsale:useritems", args=[user.id]))

def signin(request, origin_path):
    context = {
        "origin_path": origin_path,
    }
    add_context(request, context)

    return render(request, "forsale/signin.html", context)


def signin_done(request, origin_path):
    context = {
        "origin_path": origin_path,
    }
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
    if user is None:
        # No backend authenticated the credentials
        try:
            User.objects.get(username=username)
            context['signin_error'] = "Password is incorrect"
        except User.DoesNotExist:
            context['signin_error'] = f"No user found with username: {username}"

        return render(request, "forsale/signin.html", context)

    login(request, user)
    return HttpResponseRedirect(origin_path)

def signout_done(request, origin_path):
    # Logout and return to original page.
    logout(request)

    context = {
        "origin_path": origin_path,
    }
    add_context(request, context)

    return HttpResponseRedirect(origin_path)


def signup(request, origin_path):
    context = {
        "origin_path": origin_path,
        "username": request.POST['username'],
        "password": request.POST['password'],
    }
    add_context(request, context)

    return render(request, "forsale/signup.html", context)


def signup_done(request, origin_path):
    context = {
        "origin_path": origin_path,
    }
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
    return HttpResponseRedirect(origin_path)

