from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import TodoListSerializer
from .serializers import TodoSerializer
from .models import Todo

@api_view(['GET', 'POST'])
def todos(request):
    if request.method == 'POST':
        return create_todo(request)
    else:
        return get_all_todos(request)

@api_view(['GET', 'PUT'])
def todo(request, todoId):
    try:
        todo = Todo.objects.get(pk=todoId)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        return update_todo(request, todo)

    serializer = TodoSerializer(todo)
    return Response(serializer.data)

def create_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_todo(request, todo):
    serializer = TodoSerializer(todo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_all_todos(request):
    try:
        is_done = int(validate_is_done_filter(request.query_params.get('is_done', '1')))
    except ValidationError as validation_error:
        return Response({ 'errors': validation_error.message_dict }, status=status.HTTP_400_BAD_REQUEST)
    query_set = Todo.objects
    if is_done > -1:
        query_set = query_set.filter(is_done=is_done == 1)
    serializer = TodoListSerializer({ 'todos': query_set })
    return Response(serializer.data)

def validate_is_done_filter(filter):
    if filter not in ['-1', '0', '1']:
        raise ValidationError({'is_done': 'Invalid filtering on done params'})
    return filter
