from django import forms

from forsale.models import Categories


class NewItemForm(forms.Form):
    category = forms.ModelChoiceField(
        label="Category", queryset=Categories.objects, to_field_name="name"
    )
    description = forms.CharField(
        label="Description", max_length=255
    )
    price = forms.FloatField(
        label="Price $", min_value=0.0
    )

class ItemBidForm(forms.Form):
    price = forms.FloatField(
        label="Price $", min_value=0.0
    )

