"""reviews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from webapp import views as web_views
from accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', web_views.IndexView.as_view(), name="index"),
    path('products/<int:pk>/detail', web_views.ProductDetailView.as_view(), name="product_detail"),
    path('products/create', web_views.ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/edit', web_views.ProductEditView.as_view(), name="product_edit"),
    path('products/<int:pk>/delete', web_views.ProductDeleteView.as_view(), name="product_delete"),
    path('products/<int:pk>/reviews/create', web_views.ReviewCreateView.as_view(), name="review_create"),
    path('reviews/<int:pk>/edit', web_views.EditReviewView.as_view(), name="review_edit"),
    path('reviews/<int:pk>/delete', web_views.DeleteReviewView.as_view(), name="review_delete"),
    path('accounts/login/', acc_views.LoginView.as_view(), name="login"),
    path('accounts/logout/', acc_views.LogoutView.as_view(), name="logout"),
    path('accounts/register/', acc_views.RegisterView.as_view(), name="register"),
    path('accounts/<int:pk>/profile', acc_views.UserDetailView.as_view(), name="user_detail"),
    path('accounts/<int:pk>/profile/edit', acc_views.UserChangeView.as_view(), name="user_change"),
    path('accounts/<int:pk>/profile/change_password', acc_views.ChangePasswordView.as_view(), name="user_change_password")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
