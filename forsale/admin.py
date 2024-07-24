from django.contrib import admin

from .models import Categories, Items, Offers, Userinfo

admin.site.register(Categories)
admin.site.register(Items)
admin.site.register(Offers)
admin.site.register(Userinfo)

