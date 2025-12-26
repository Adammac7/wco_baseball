"use client";

import { ReactNode } from "react";
import { Search, Filter, Inbox } from "lucide-react";

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description: string;
  action?: ReactNode;
  type?: "search" | "filter" | "default";
}

export function EmptyState({
  icon,
  title,
  description,
  action,
  type = "default",
}: EmptyStateProps) {
  const defaultIcons = {
    search: <Search className="w-16 h-16 text-gray-600" />,
    filter: <Filter className="w-16 h-16 text-gray-600" />,
    default: <Inbox className="w-16 h-16 text-gray-600" />,
  };

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="mb-6 opacity-50 animate-fade-in-up">
        {icon || defaultIcons[type]}
      </div>
      <h3 className="text-xl font-semibold text-white mb-2 animate-fade-in-up" style={{ animationDelay: "0.1s" }}>
        {title}
      </h3>
      <p className="text-gray-400 text-center max-w-md mb-6 animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
        {description}
      </p>
      {action && (
        <div className="animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
          {action}
        </div>
      )}
    </div>
  );
}

