from rest_framework import serializers

from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class TodoListSerializer(serializers.Serializer):
    todos = TodoSerializer(many=True)