from rest_framework import serializers
from .models import TaskDependency


class TaskDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDependency
        fields = ['id', 'task', 'depends_on', 'created_at']
        read_only_fields = ['id', 'created_at', 'task']
