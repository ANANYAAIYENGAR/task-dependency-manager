1. Circular Dependency Detection Algorithm

To detect circular dependencies between tasks, the system models tasks and their dependencies as a directed graph, where each task is a node and each dependency is a directed edge.

When a new dependency is added, the system performs a Depth-First Search (DFS) starting from the dependency node to check whether the target task can be reached again. If the target task is encountered during traversal, it indicates a cycle.

The algorithm also keeps track of the recursion path, allowing the system to return the exact circular dependency path (e.g., [1, 3, 5, 1]) when a cycle is detected. If a cycle is found, the dependency is rejected and not saved.

Time Complexity:The time complexity of the algorithm is O(V + E), where:
V is the number of tasks
E is the number of dependencies
This approach is efficient and scales well for the expected number of tasks (20–30).

2. Most Challenging Part and How It Was Solved

The most challenging part of the project was correctly visualizing task dependencies using SVG without external graph libraries.

Specifically, ensuring that arrowheads did not overlap task nodes was non-trivial. This issue was solved by applying vector math to shorten arrow lines so that arrowheads terminate just outside the node boundaries. This ensured clean, readable visuals regardless of arrow direction.

Another challenge was handling real-time dependency updates and ensuring task statuses updated correctly when dependencies changed. This was solved by centralizing the status update logic in the backend and re-evaluating dependent tasks whenever a task’s status was updated.

3. Improvements with More Time

Given more time, the following improvements could be made:
Add drag-and-drop support for repositioning nodes in the graph
Implement zoom and pan functionality for large dependency graphs
Highlight dependencies when a task node is clicked
Add task priority levels and estimated completion time
Improve concurrency handling for simultaneous task updates
Allow exporting the dependency graph as an image