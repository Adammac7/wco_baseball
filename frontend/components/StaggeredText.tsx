"use client";

import { ReactNode } from "react";

interface StaggeredTextProps {
  children: ReactNode;
  className?: string;
  staggerDelay?: number;
}

export function StaggeredText({
  children,
  className = "",
  staggerDelay = 0.1,
}: StaggeredTextProps) {
  const words = typeof children === "string" ? children.split(" ") : [children];

  return (
    <span className={className}>
      {words.map((word, index) => (
        <span
          key={index}
          className="inline-block animate-fade-in-up"
          style={{
            animationDelay: `${index * staggerDelay}s`,
            opacity: 0,
          }}
        >
          {word}
          {index < words.length - 1 && "\u00A0"}
        </span>
      ))}
    </span>
  );
}

