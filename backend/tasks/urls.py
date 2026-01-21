from django.urls import path
from .views import AddTaskDependencyView

urlpatterns = [
    path(
        'tasks/<int:task_id>/dependencies/',
        AddTaskDependencyView.as_view(),
        name='add-task-dependency'
    ),
]
