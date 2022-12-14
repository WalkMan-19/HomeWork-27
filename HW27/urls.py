"""HW27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from HW27 import settings
from ads import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', lambda request: JsonResponse({"status": "ok"}, status=200)),

    path('cat/', views.CategoryListView.as_view()),
    path('cat/<int:pk>', views.CategoryDetailView.as_view()),
    path('cat/create/', views.CategoryCreateView.as_view()),
    path('cat/update/<int:pk>', views.CategoryUpdateView.as_view()),
    path('cat/delete/<int:pk>', views.CategoryDeleteView.as_view()),

    path('ad/', include('ads.urls')),

    path('loc/', views.LocationListView.as_view()),
    path('loc/<int:pk>', views.LocationDetailView.as_view()),
    path('loc/create/', views.LocationCreateView.as_view()),
    path('loc/delete/<int:pk>', views.LocationDeleteView.as_view()),

    path('user/', views.UserListView.as_view()),
    path('user/<int:pk>', views.UserDetailView.as_view()),
    path('user/create/', views.UserCreateView.as_view()),
    path('user/update/<int:pk>', views.UserUpdateView.as_view()),
    path('user/delete/<int:pk>', views.UserDeleteView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
