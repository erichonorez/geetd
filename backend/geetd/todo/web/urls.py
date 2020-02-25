from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="web-todo-list")
]
