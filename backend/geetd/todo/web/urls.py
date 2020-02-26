from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="web-todo-list"),
    path('todos/create', views.CreateTodoView.as_view(), name='web-todo-create'),
    path('todos/<uuid:todo_id>', views.UpdateTodoView.as_view(), name='web-todo-update'),
    path('todos/toggle-complete', views.ToggleCompleteView.as_view(), name='web-todo-toggle-complete')
]
