from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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


class ProductEditView(UpdateView):
    model = Product
    template_name = "products/edit.html"
    form_class = ProductForm
    success_url = reverse_lazy("index")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/delete.html"
    success_url = reverse_lazy("index")
