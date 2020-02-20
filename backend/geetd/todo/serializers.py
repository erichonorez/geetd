from rest_framework import serializers

from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['state', 'priority_order']

class ChangeTodoStateSerializer(serializers.Serializer):
    state = serializers.ChoiceField(choices=Todo.STATES)