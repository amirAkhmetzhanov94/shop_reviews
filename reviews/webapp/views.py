from django.shortcuts import render
from django.views.generic import ListView, DetailView

from webapp.models import Product


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"
