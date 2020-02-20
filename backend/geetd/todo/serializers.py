from rest_framework import serializers

from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['priority_order']

class PriorityzeTodoSerializer(serializers.Serializer):
    priority_order = serializers.IntegerField(min_value=0)