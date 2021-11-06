from django.forms import widgets
from django import forms

from webapp.models import Product


class ProductForm(forms.ModelForm):
    name = forms.CharField()
    category = forms.CharField(widget=widgets.Select(choices=Product.CATEGORY_CHOICES))
    description = forms.CharField(widget=widgets.Textarea)
    picture = forms.ImageField()

    class Meta:
        model = Product
        exclude = []
