
from rest_framework import serializers
from todos.models import Todos

class TodosSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Todos
        fields = [
            'id',
            'user',
            'title',
            'description',
            'priority',
            'is_completed',   
            'is_archived',
            'due_date',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']