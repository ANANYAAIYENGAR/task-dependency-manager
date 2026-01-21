# Task Dependency Management System

A full-stack Task Dependency Management System that allows users to create tasks, define dependencies between them, automatically manage task statuses, detect circular dependencies, and visualize task relationships using an interactive graph.

This project focuses on **correct dependency logic, clean backend APIs, and clear frontend visualization**, without relying on external graph libraries.

---

## 🚀 Features

### ✅ Task Management
- Create tasks with title and description
- Update task status (`pending`, `in_progress`, `completed`, `blocked`)
- Delete tasks with dependency warnings

### 🔗 Dependency Handling
- Add multiple dependencies per task
- Prevent self-dependencies
- Detect circular dependencies using DFS
- Return exact circular path when a cycle is detected

### 🔄 Automatic Status Updates
- If all dependencies are completed → task becomes `in_progress`
- If any dependency is blocked → task becomes `blocked`
- If dependencies exist but are incomplete → task remains `pending`
- Status changes propagate to dependent tasks

### 📊 Graph Visualization
- SVG-based dependency graph (no external graph libraries)
- Tasks displayed as nodes
- Dependencies displayed as directional arrows
- Color-coded nodes by status
- Legend for easy interpretation

---

## 🛠 Tech Stack

### Backend
- Django 4.x
- Django REST Framework
- MySQL 8.0
- Python 3.x

### Frontend
- React 18 (Vite)
- JavaScript
- Tailwind CSS
- SVG for graph visualization

---

## 📁 Project Structure

task-dependency-manager/
├── backend/
│ ├── config/
│ ├── tasks/
│ └── manage.py
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ └── DependencyGraph.jsx
│ │ ├── App.jsx
│ │ └── main.jsx
├── README.md
├── DECISIONS.md
└── .gitignore

## ⚙️ Backend Setup

```bash
cd backend
python -m venv env
env\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Backend runs at: http://127.0.0.1:8000/

Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at: http://localhost:5173/

🔌 API Endpoints
Add Dependency
POST /api/tasks/{task_id}/dependencies/


Request body:

{
  "depends_on_id": 5
}


Error (circular dependency):

{
  "error": "Circular dependency detected",
  "path": [1, 3, 5, 1]
}

Update Task Status
PATCH /api/tasks/{task_id}/


Request body:

{
  "status": "completed"
}