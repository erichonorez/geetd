import django_filters.rest_framework

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import TodoSerializer
from .serializers import ChangeTodoStateSerializer
from .models import Todo

class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['is_done', 'state']

class TodoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class =  TodoSerializer

class ChangeTodoStateView(generics.GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = ChangeTodoStateSerializer
    def post(self, request, pk):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        try:
            todo = self.get_queryset().get(pk=pk)
        except Todo.DoesNotExists:
            return NotFound()
        todo.move_to_state(serializer.validated_data['state'])
        todo.save()
        return Response(serializer.data)