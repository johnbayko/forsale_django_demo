from django.contrib import admin

from .models import Categories, Items, Userinfo

admin.site.register(Categories)
admin.site.register(Items)
admin.site.register(Userinfo)

