from django.urls import path
from django.conf.urls import url

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

schema_view = get_schema_view(
   openapi.Info(
      title="Todo API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('todos', views.TodoListView.as_view()),
    path('todos/<uuid:pk>', views.TodoView.as_view()),
    path('doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-redoc'),
]