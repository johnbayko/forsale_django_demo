from django.db import models
from django.db.models import Q
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

    @property
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


class ItemsManager(models.Manager):
    def get_queryset(self):
        # Thanks ChatGPT.
        # Use Exists to annotate with a boolean indicating if there are any
        # accepted offers
        return super().get_queryset().annotate(
            sold=models.Exists(
                # Subquery to check if there are any accepted offers for each
                # item
                Offers.objects.filter(
                    item=models.OuterRef('pk'),
                    accepted=True
                ).values('id')
            )
        )

class Items(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Userinfo, on_delete=models.PROTECT)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT)
    description = models.CharField(max_length=256, blank=True)
#    picture = models.ImageField(upload_to=)

    # Price is in cents. Barring hyperinflation, should be big enough.
    price = models.IntegerField()

    removed = models.BooleanField(default=False, null=False)

    objects = ItemsManager()


class Offers(models.Model):
    item = models.ForeignKey(Items, related_name="offers", on_delete=models.PROTECT)
    userinfo = models.ForeignKey(Userinfo, on_delete=models.PROTECT)

    price = models.IntegerField()

    # Offer accepted. Allow only one. Can be withdrawn until delivered.
    accepted = models.BooleanField(default=False, null=False)

    # Item delivered. Only if accepted (imlies only one).
#    delivered = models.BooleanField(default=False, null=False)

    class Meta:
        constraints = [
            # Only one per item can be accepted.
            models.UniqueConstraint(
                fields=['item'],
                condition=Q(accepted=True),
                name='accepted_unique'
            ),
#            # Can be delivered only if accepted.
#            models.CheckConstraint(
#                check=Q(delivered=F('accepted')) | Q(delivered=False),
#                name='delivered_accepted'
#            ).
        ]

