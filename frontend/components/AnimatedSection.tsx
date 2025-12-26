"use client";

import { useEffect, useRef, useState, ReactNode } from "react";

interface AnimatedSectionProps {
  children: ReactNode;
  delay?: number;
  direction?: "up" | "down" | "left" | "right" | "scale";
  className?: string;
  threshold?: number;
}

export function AnimatedSection({
  children,
  delay = 0,
  direction = "up",
  className = "",
  threshold = 0.1,
}: AnimatedSectionProps) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Only trigger once - if already visible, don't observe
    if (isVisible) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setTimeout(() => {
            setIsVisible(true);
            // Unobserve after triggering to prevent re-triggering
            if (ref.current) {
              observer.unobserve(ref.current);
            }
          }, delay);
        }
      },
      { threshold }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [delay, threshold, isVisible]);

  const directionClasses = {
    up: "animate-fade-in-up",
    down: "animate-fade-in-down",
    left: "animate-slide-in-left",
    right: "animate-slide-in-right",
    scale: "animate-fade-in-scale",
  };

  return (
    <div
      ref={ref}
      className={`${className} ${isVisible ? directionClasses[direction] : "opacity-0"}`}
    >
      {children}
    </div>
  );
}

