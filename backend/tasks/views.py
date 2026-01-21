from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, TaskDependency
from .serializers import TaskDependencySerializer
from .utils import detect_cycle, build_dependency_graph

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
            path.append(depends_on_id)
            return Response(
                {
                    "error": "Circular dependency detected",
                    "path": path
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
