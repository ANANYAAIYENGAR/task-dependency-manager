# Design Decisions – Task Dependency Management System

This document explains the key technical and architectural decisions made while building the Task Dependency Management System.

---

## 1. Circular Dependency Detection

### Why DFS?
Tasks and their dependencies naturally form a **directed graph**, where:
- Each task is a node
- Each dependency is a directed edge (depends_on → task)

To detect circular dependencies, I used **Depth-First Search (DFS)** because:
- DFS is well-suited for cycle detection in directed graphs
- It allows tracking the exact traversal path
- It efficiently detects back-edges, which indicate cycles

### How the Algorithm Works
1. Build an adjacency list from existing task dependencies
2. Temporarily add the new dependency edge
3. Start DFS from the dependency node
4. If during traversal the target task is encountered again, a cycle exists
5. Maintain a recursion stack to record the path
6. If a cycle is found, return both:
   - `True`
   - The exact circular path (e.g., `[1, 3, 5, 1]`)

If a cycle is detected, the dependency is **not saved** and an error response is returned.

### Time Complexity
- **O(V + E)** where:
  - `V` = number of tasks
  - `E` = number of dependencies
- This is optimal for graph traversal and scales well for 20–30 tasks

---

## 2. Automatic Task Status Updates

Task status is automatically updated based on dependency states.

### Rules Implemented
- If **all dependencies are completed** → task becomes `in_progress`
- If **any dependency is blocked** → task becomes `blocked`
- If dependencies exist but are not all completed → task remains `pending`
- When a task is marked `completed`, all dependent tasks are re-evaluated

This logic ensures:
- Tasks cannot start before prerequisites are satisfied
- Status changes propagate correctly through the dependency graph

---

## 3. Graph Visualization Choice (SVG vs Canvas)

### Why SVG?
For visualizing task dependencies, I chose **SVG** instead of Canvas because:
- SVG elements are declarative and easier to manage in React
- Arrows, markers, and text labels are simpler to implement
- Individual nodes and edges can be styled and interacted with easily
- SVG scales well for small to medium-sized graphs (20–30 tasks)

### Layout Strategy
- A simple **top-to-bottom hierarchical layout** was used
- Nodes are vertically spaced to maintain readability
- Arrows are drawn from **dependency → dependent task**
- Vector math is used to shorten edges so arrowheads never overlap nodes

This approach prioritizes **clarity and correctness** over complex animations.

---

## 4. Backend–Frontend Integration

- Backend exposes REST APIs using Django REST Framework
- Frontend fetches task and dependency data via `/api/graph/`
- CORS is enabled using `django-cors-headers` for local development
- No external graph libraries were used, as required

---

## 5. Trade-offs and Future Improvements

### Trade-offs
- Chose a simple layout instead of force-directed graphs to reduce complexity
- De-duplication of dependencies is handled on the frontend for clean rendering

### Possible Improvements
- Drag-and-drop repositioning of nodes
- Zoom and pan functionality
- Highlight dependencies on node click
- Export graph as an image
- Task priority and estimated completion time

---

## Conclusion

The system focuses on **correct dependency handling, clear visualization, and clean architecture**.  
All design choices were made to balance simplicity, correctness, and extensibility while meeting the project requirements.
