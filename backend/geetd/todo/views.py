import django_filters.rest_framework

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .serializers import TodoSerializer
from .serializers import PriorityzeTodoSerializer
from .models import Todo

class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['is_done', 'state']

class TodoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class =  TodoSerializer

class PrioritizeTodoView(generics.GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = PriorityzeTodoSerializer

    def put(self, request, pk):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        try:
            todo = self.get_queryset().get(pk=pk)
        except Todo.DoesNotExist:
            return NotFound()
        todo.prioritize(serializer.validated_data['priority_order'])
        return Response(serializer.data)