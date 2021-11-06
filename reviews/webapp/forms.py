from django.forms import widgets
from django import forms

from webapp.models import Product, Review


class ProductForm(forms.ModelForm):
    name = forms.CharField()
    category = forms.CharField(widget=widgets.Select(choices=Product.CATEGORY_CHOICES))
    description = forms.CharField(widget=widgets.Textarea)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Product
        exclude = []


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=widgets.Textarea)

    class Meta:
        model = Review
        exclude = ["author", "product"]
