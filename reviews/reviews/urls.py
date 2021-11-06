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

urlpatterns = [
    path('admin', admin.site.urls),
    path('', web_views.IndexView.as_view(), name="index"),
    path('products/<int:pk>/detail', web_views.ProductDetailView.as_view(), name="product_detail"),
    path('products/create', web_views.ProductCreateView.as_view(), name="product_create"),
    path('products/<int:pk>/edit', web_views.ProductEditView.as_view(), name="product_edit")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
