export default function DependencyGraph() {
  const tasks = [
    { id: 1, title: "Task A", status: "in_progress", y: 100 },
    { id: 2, title: "Task B", status: "completed", y: 250 },
    { id: 3, title: "Task C", status: "in_progress", y: 400 },
  ];

  const statusColors = {
    pending: "#9ca3af",
    in_progress: "#3b82f6",
    completed: "#22c55e",
    blocked: "#ef4444",
  };

  const cx = 250;   // center X for nodes
  const r = 30;     // node radius

  return (
    <div style={{ display: "flex", gap: "40px", alignItems: "flex-start" }}>
      
      {/* SVG GRAPH */}
      <svg
        width="500"
        height="500"
        style={{ border: "2px solid #ccc", background: "#fff" }}
      >
        {/* Arrow marker */}
        <defs>
          <marker
            id="arrow"
            markerWidth="12"
            markerHeight="12"
            refX="10"
            refY="6"
            orient="auto"
          >
            <path d="M0,0 L12,6 L0,12 Z" fill="#000" />
          </marker>
        </defs>

        {/* Arrows */}
        <line
          x1={cx}
          y1={250 - r}
          x2={cx}
          y2={100 + r}
          stroke="black"
          strokeWidth="2"
          markerEnd="url(#arrow)"
        />

        <line
          x1={cx}
          y1={250 + r}
          x2={cx}
          y2={400 - r}
          stroke="black"
          strokeWidth="2"
          markerEnd="url(#arrow)"
        />

        {/* Nodes */}
        {tasks.map((task) => (
          <g key={task.id}>
            <circle
              cx={cx}
              cy={task.y}
              r={r}
              fill={statusColors[task.status]}
            />
            <text
              x={cx}
              y={task.y + 5}
              textAnchor="middle"
              fill="#fff"
              fontSize="13"
              fontWeight="bold"
            >
              {task.title}
            </text>
          </g>
        ))}
      </svg>

      {/* LEGEND */}
      <div
        style={{
          border: "1px solid #ccc",
          padding: "16px",
          width: "220px",
          background: "#fff",
        }}
      >
        <h3 style={{ marginBottom: "12px" }}>Legend</h3>

        <div style={{ marginBottom: "8px", color: "#9ca3af" }}>
          ● Pending
        </div>
        <div style={{ marginBottom: "8px", color: "#3b82f6" }}>
          ● In Progress
        </div>
        <div style={{ marginBottom: "8px", color: "#22c55e" }}>
          ● Completed
        </div>
        <div style={{ color: "#ef4444" }}>
          ● Blocked
        </div>
      </div>
    </div>
  );
}
