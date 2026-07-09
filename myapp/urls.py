"""
URL configuration for Genesis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home
    path("", views.index, name="home"),

    path("home/", views.index, name="index"),

    path("contact/", views.home, name="contact"),



    # Blog
    path("blog/", views.blog, name="blog"),

    # Blog Details
    path("details/", views.details, name="details"),

    # Services
    path("services/", views.services, name="services"),

    # Starter Page
    path("starter/", views.starter, name="starter"),

    # Error Page
    path("error/", views.error, name="error"),

    path("show/", views.show, name="show"),

    path('edit/<int:id>/', views.edit,),

    # path('delete/<int:id>/', views.delete_contact, name='delete_contact'),

    path('delete/<int:id>/', views.delete),

    # path("undo-delete/", views.undo_delete, name="undo_delete"),

    # mpesa urls #
    path('payment/', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),

]
