from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="web-todo-list"),
    path('todos/create', views.CreateTodoView.as_view(), name='web-todo-create'),
    path('todos/<uuid:todo_id>', views.DetailTodoView.as_view(), name='web-todo-update'),
    path('todos/<uuid:todo_id>/prioritize', views.PrioritizeTodoView.as_view(), name='web-todo-prioritize'),
    path('todos/<uuid:todo_id>/toggle-complete', views.ToggleCompleteView.as_view(), name='web-todo-toggle-complete'),
    path('todos/<uuid:todo_id>/delete', views.DeleteTodoView.as_view(), name='web-todo-delete'),
    path('todos/archive', views.ArchiveTodosInStateView.as_view(), name='web-todo-archive'),
    path('todos/archived', views.ArchivedTodosView.as_view(), name='web-todo-archived'),
]
