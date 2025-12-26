"use client";

import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface StatBadgeProps {
  value: number | string;
  label: string;
  trend?: "up" | "down" | "neutral";
  trendValue?: number;
  className?: string;
  color?: "red" | "green" | "yellow" | "blue";
}

export function StatBadge({
  value,
  label,
  trend,
  trendValue,
  className = "",
  color = "red",
}: StatBadgeProps) {
  const colorClasses = {
    red: "from-red-900/30 to-red-800/20 border-red-800/50 text-red-400",
    green: "from-green-900/30 to-green-800/20 border-green-800/50 text-green-400",
    yellow: "from-yellow-900/30 to-yellow-800/20 border-yellow-800/50 text-yellow-400",
    blue: "from-blue-900/30 to-blue-800/20 border-blue-800/50 text-blue-400",
  };

  const trendIcons = {
    up: <TrendingUp className="w-3 h-3" />,
    down: <TrendingDown className="w-3 h-3" />,
    neutral: <Minus className="w-3 h-3" />,
  };

  return (
    <div
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-gradient-to-br ${colorClasses[color]} border text-xs font-medium ${className}`}
    >
      <span className="font-semibold">{value}</span>
      <span className="text-gray-300">{label}</span>
      {trend && trendValue !== undefined && (
        <span className="flex items-center gap-1 text-gray-400">
          {trendIcons[trend]}
          <span>{Math.abs(trendValue)}%</span>
        </span>
      )}
    </div>
  );
}

