def detect_cycle(start_id, target_id, graph, visited, path):
    """
    Detects if a path exists from start_id to target_id using DFS.

    Returns:
        (bool, list) -> (cycle_found, path)
    """

    visited.add(start_id)
    path.append(start_id)

    # If we reached the original task, cycle exists
    if start_id == target_id:
        return True, path.copy()

    # Traverse neighbors
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

    # Backtrack
    path.pop()
    return False, []

from .models import TaskDependency


def build_dependency_graph():
    """
    Builds adjacency list of task dependencies.
    Returns:
        dict -> {task_id: [depends_on_id, ...]}
    """
    graph = {}

    dependencies = TaskDependency.objects.all()

    for dep in dependencies:
        task_id = dep.task_id
        depends_on_id = dep.depends_on_id

        if task_id not in graph:
            graph[task_id] = []

        graph[task_id].append(depends_on_id)

    return graph
