from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=256, blank=True)


class Items(models.Model):
    created = models.DateTimeField(auto_now_add=True)
#    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    description = models.CharField(max_length=256, blank=True)
#    picture = models.ImageField(upload_to=)

    # Price is in cents. Barring hyperinflation, should be big enough.
    price = models.IntegerField()

    sold = models.BooleanField(default=False, null=False)
    removed = models.BooleanField(default=False, null=False)

