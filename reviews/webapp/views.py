from django.shortcuts import render
from django.views.generic import ListView

from webapp.models import Product


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"