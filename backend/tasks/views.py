from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, TaskDependency
from .serializers import TaskDependencySerializer
from .utils import (
    detect_cycle,
    build_dependency_graph,
    update_task_status,
    update_dependent_tasks
)

class TaskGraphView(APIView):

    def get(self, request):
        tasks = Task.objects.all().values("id", "title", "status")
        dependencies = TaskDependency.objects.all().values(
            "task_id", "depends_on_id"
        )

        return Response({
            "tasks": list(tasks),
            "dependencies": list(dependencies)
        })

class AddTaskDependencyView(APIView):

    def post(self, request, task_id):
        depends_on_id = request.data.get('depends_on_id')

        if not depends_on_id:
            return Response(
                {"error": "depends_on_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(task_id) == int(depends_on_id):
            return Response(
                {"error": "Task cannot depend on itself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id)
            depends_on = Task.objects.get(id=depends_on_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Build current graph
        graph = build_dependency_graph()

        # Add the new edge temporarily
        graph.setdefault(task_id, []).append(depends_on_id)

        # Run DFS from depends_on → task
        cycle_found, path = detect_cycle(
            start_id=depends_on_id,
            target_id=task_id,
            graph=graph,
            visited=set(),
            path=[]
        )

        if cycle_found:
            return Response(
                {
                    "error": "Circular dependency detected",
                    "path": path + [depends_on_id]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save dependency
        dependency = TaskDependency.objects.create(
            task=task,
            depends_on=depends_on
        )

        serializer = TaskDependencySerializer(dependency)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTaskStatusView(APIView):

    def patch(self, request, task_id):
        new_status = request.data.get('status')

        if new_status not in ['pending', 'in_progress', 'completed', 'blocked']:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task.status = new_status
        task.save()

        # Update dependent tasks if task is completed or blocked
        if new_status in ['completed', 'blocked']:
            update_dependent_tasks(task)

        return Response(
            {
                "id": task.id,
                "status": task.status
            },
            status=status.HTTP_200_OK
        )
