import { useEffect, useState } from "react";

const statusColors = {
  pending: "#9ca3af",
  in_progress: "#3b82f6",
  completed: "#22c55e",
  blocked: "#ef4444",
};

export default function DependencyGraph() {
  const [data, setData] = useState({ tasks: [], dependencies: [] });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/graph/")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error(err));
  }, []);

  const nodeRadius = 25;
  const verticalGap = 120;
  const centerX = 300;

  // Position nodes
  const positions = {};
  data.tasks.forEach((task, index) => {
    positions[task.id] = {
      x: centerX,
      y: 80 + index * verticalGap,
    };
  });

  // Remove duplicate dependencies
  const uniqueDependencies = Array.from(
    new Map(
      data.dependencies.map((d) => [
        `${d.depends_on_id}-${d.task_id}`,
        d,
      ])
    ).values()
  );

  // Helper to shorten line so arrow never enters circle
  function shortenLine(x1, y1, x2, y2, offset) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const length = Math.sqrt(dx * dx + dy * dy);

    const ratio = (length - offset) / length;

    return {
      x: x1 + dx * ratio,
      y: y1 + dy * ratio,
    };
  }

  return (
    <svg width="600" height="600" className="border bg-white">
      {/* Arrow marker */}
      <defs>
        <marker
          id="arrow"
          markerWidth="12"
          markerHeight="12"
          refX="10"
          refY="6"
          orient="auto"
          markerUnits="strokeWidth"
        >
          <path d="M0,0 L12,6 L0,12 Z" fill="#000" />
        </marker>
      </defs>

      {/* Draw arrows */}
      {uniqueDependencies.map((dep, index) => {
        const from = positions[dep.depends_on_id]; // dependency
        const to = positions[dep.task_id];         // dependent
        if (!from || !to) return null;

        // Shorten arrow end so arrowhead stays outside circle
        const end = shortenLine(
          from.x,
          from.y,
          to.x,
          to.y,
          nodeRadius + 10
        );

        return (
          <line
            key={index}
            x1={from.x}
            y1={from.y}
            x2={end.x}
            y2={end.y}
            stroke="#000"
            strokeWidth="2"
            markerEnd="url(#arrow)"
          />
        );
      })}

      {/* Draw nodes */}
      {data.tasks.map((task) => {
        const pos = positions[task.id];
        return (
          <g key={task.id}>
            <circle
              cx={pos.x}
              cy={pos.y}
              r={nodeRadius}
              fill={statusColors[task.status]}
            />
            <text
              x={pos.x}
              y={pos.y + 5}
              textAnchor="middle"
              fill="#fff"
              fontSize="12"
              fontWeight="bold"
            >
              {task.title}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
