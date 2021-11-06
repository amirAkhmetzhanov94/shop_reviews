from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import ProductForm, ReviewForm
from webapp.models import Product, Review


class IndexView(ListView):
    model = Product
    template_name = "products/index.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ratings_list = []
        for product in self.object_list:
            ratings_list.append(self.find_avg(product))
        context["ratings_list"] = ratings_list[::-1]
        return context

    def find_avg(self, product):
        avg_rating = product.reviews.values("rating").aggregate(Avg("rating")).get("rating__avg")
        if avg_rating is None:
            avg_rating = 0
        else:
            avg_rating = round(avg_rating, 2)
        return avg_rating


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product_id__exact=self.object.pk)
        context["review_form"] = ReviewForm()
        avg_rating = self.object.reviews.values("rating").aggregate(Avg("rating")).get("rating__avg")
        if avg_rating is None:
            context["avg_rating"] = 0
        else:
            context["avg_rating"] = round(avg_rating, 2)
        return context


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


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = "products/detail.html"
    form_class = ReviewForm

    def get_product(self):
        return get_object_or_404(Product, pk=self.kwargs.get("pk"))

    def form_valid(self, form):
        form.instance.product = self.get_product()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("product_detail", kwargs={"pk": self.get_product().pk})


class EditReviewView(UserPassesTestMixin, UpdateView):
    template_name = "reviews/update.html"
    form_class = ReviewForm
    model = Review

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.groups.filter(name='Moderator').exists()

    def get_success_url(self):
        return reverse("product_detail", kwargs={"pk": self.get_object().product.pk})


class DeleteReviewView(UserPassesTestMixin, DeleteView):
    template_name = "reviews/delete.html"
    model = Review

    def test_func(self):
        return self.request.user == self.get_object() or self.request.user.groups.filter(name='Moderator').exists()

    def get_success_url(self):
        return reverse("product_detail", kwargs={"pk": self.get_object().product.pk})
