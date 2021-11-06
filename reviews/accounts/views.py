from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from accounts.forms import RegistrationForm, UserChangeForm, PasswordChangeForm
from webapp.models import Review


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "registration/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_path = request.POST.get("next")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_path:
                return HttpResponseRedirect(next_path)
            return redirect("index")
        return render(request, "registration/login.html", {"has_error": True})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("index")


class RegisterView(CreateView):
    model = get_user_model()
    template_name = "registration/register.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('index')
        return next_url


class UserDetailView(DetailView, MultipleObjectMixin):
    model = get_user_model()
    template_name = "user_detail.html"
    context_object_name = "user_obj"

    def get_context_data(self, **kwargs):
        object_list = Review.objects.filter(author__username__icontains=self.object.username)
        context = super(UserDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = "edit_profile.html"
    context_object_name = "user_obj"

    def test_func(self):
        return self.request.user == self.get_object()

    def get_success_url(self):
        return reverse("user_detail", kwargs={"pk": self.object.pk})


class ChangePasswordView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = PasswordChangeForm
    template_name = "change_password.html"
    context_object_name = "user_obj"

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.instance)
        return redirect("user_detail", pk=self.get_object().pk)

    def test_func(self):
        return self.request.user == self.get_object()
