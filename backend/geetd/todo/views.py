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
        validated_done_file = validate_done_filter(request.GET.get('done', '1'))
    except ValidationError as validation_error:
        return Response(validation_error.message_dict(), status=status.HTTP_400_BAD_REQUEST)
        
    serializer = TodoListSerializer({ 'todos': Todo.objects.all() })
    return Response(serializer.data)

def validate_done_filter(filter):
    if filter not in ['-1', '0', '1']:
        raise ValidationError('Invalid filtering on done params', code='done')
