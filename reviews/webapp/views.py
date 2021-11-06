from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from webapp.forms import ProductForm
from webapp.models import Product


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "products/create.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse("index")
