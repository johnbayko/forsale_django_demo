from django.db import models
from django.contrib.auth.models import User

class Categories(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name


class Userinfo(models.Model):
    # User table is out managed by Django, so can't prevent deletions.
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # If user was deleted, this retains original user identity.
    username = models.CharField(max_length=150)

    # Address is optional until buying.
    address = models.CharField(max_length=256, blank=True)

    def display_name(self):
        user = self.user
        if user is None:
            # Could have been deleted. Use stored info.
            # username now, could be more added.
            return username

        namelist = []
        if user.first_name != '':
            namelist.append(user.first_name)

        if user.last_name != '':
            namelist.append(user.last_name)

        if len(namelist) == 0:
            # No actual name, use username.
            namelist.append(user.username)

        return " ".join(namelist)


class Items(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Userinfo, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    description = models.CharField(max_length=256, blank=True)
#    picture = models.ImageField(upload_to=)

    # Price is in cents. Barring hyperinflation, should be big enough.
    price = models.IntegerField()

    sold = models.BooleanField(default=False, null=False)
    removed = models.BooleanField(default=False, null=False)


class Offers(models.Model):
    item = models.ForeignKey(Items, related_name="offers", on_delete=models.PROTECT)
    userinfo = models.ForeignKey(Userinfo, on_delete=models.PROTECT)

    price = models.IntegerField()

    accepted = models.BooleanField(default=False, null=False)

