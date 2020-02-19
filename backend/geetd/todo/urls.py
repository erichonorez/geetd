from django.urls import path
from . import views

urlpatterns = [
    path('todos', views.todos),
    path('todos/<uuid:todoId>', views.todo)
]