from .models import Task, TaskDependency


def detect_cycle(start_id, target_id, graph, visited, path):
    visited.add(start_id)
    path.append(start_id)

    if start_id == target_id:
        return True, path.copy()

    for neighbor in graph.get(start_id, []):
        if neighbor not in visited:
            found, cycle_path = detect_cycle(
                neighbor,
                target_id,
                graph,
                visited,
                path
            )
            if found:
                return True, cycle_path

    path.pop()
    return False, []


def build_dependency_graph():
    graph = {}
    dependencies = TaskDependency.objects.all()

    for dep in dependencies:
        graph.setdefault(dep.task_id, []).append(dep.depends_on_id)

    return graph


def update_task_status(task):
    dependencies = TaskDependency.objects.filter(task=task)

    if not dependencies.exists():
        return

    dep_statuses = [dep.depends_on.status for dep in dependencies]

    if 'blocked' in dep_statuses:
        task.status = 'blocked'
    elif all(status == 'completed' for status in dep_statuses):
        task.status = 'in_progress'
    else:
        task.status = 'pending'

    task.save()


def update_dependent_tasks(task):
    relations = TaskDependency.objects.filter(depends_on=task)

    for rel in relations:
        update_task_status(rel.task)
