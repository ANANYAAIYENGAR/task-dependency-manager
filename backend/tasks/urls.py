from django.urls import path
from .views import AddTaskDependencyView

urlpatterns = [
    path(
        'tasks/<int:task_id>/dependencies/',
        AddTaskDependencyView.as_view(),
        name='add-task-dependency'
    ),
]

from .views import UpdateTaskStatusView

urlpatterns += [
    path(
        'tasks/<int:task_id>/',
        UpdateTaskStatusView.as_view(),
        name='update-task-status'
    ),
]

from .views import TaskGraphView

urlpatterns += [
    path(
        'graph/',
        TaskGraphView.as_view(),
        name='task-graph'
    ),
]

