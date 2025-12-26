"use client";

import { LucideIcon } from "lucide-react";

interface AnimatedIconProps {
  icon: LucideIcon;
  delay?: number;
  glowColor?: "red" | "blue" | "purple" | "orange";
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function AnimatedIcon({
  icon: Icon,
  delay = 0,
  glowColor = "red",
  size = "md",
  className = "",
}: AnimatedIconProps) {
  const sizeClasses = {
    sm: "w-16 h-16",
    md: "w-20 h-20",
    lg: "w-24 h-24",
  };

  const iconSizes = {
    sm: "w-8 h-8",
    md: "w-10 h-10",
    lg: "w-12 h-12",
  };

  const glowColors = {
    red: { main: "rgba(220, 38, 38, 0.4)", accent: "rgba(220, 38, 38, 0.6)", light: "rgba(220, 38, 38, 0.2)" },
    blue: { main: "rgba(37, 99, 235, 0.4)", accent: "rgba(37, 99, 235, 0.6)", light: "rgba(37, 99, 235, 0.2)" },
    purple: { main: "rgba(147, 51, 234, 0.4)", accent: "rgba(147, 51, 234, 0.6)", light: "rgba(147, 51, 234, 0.2)" },
    orange: { main: "rgba(249, 115, 22, 0.4)", accent: "rgba(249, 115, 22, 0.6)", light: "rgba(249, 115, 22, 0.2)" },
  };

  const colors = glowColors[glowColor];

  return (
    <div
      className={`relative ${sizeClasses[size]} mx-auto mb-8 ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      {/* Outer container - sleek metallic frame */}
      <div
        className="absolute inset-0 rounded-2xl animate-fade-in-scale"
        style={{
          animationDelay: `${delay}ms`,
          background: "linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 50%, #1a1a1a 100%)",
          border: "1px solid rgba(255, 255, 255, 0.1)",
          boxShadow: `
            inset 0 1px 0 rgba(255, 255, 255, 0.15),
            inset 0 -1px 0 rgba(0, 0, 0, 0.5),
            0 0 30px ${colors.main},
            0 0 60px ${colors.light}
          `,
        }}
      />
      
      {/* Inner glow - emanating from center */}
      <div
        className="absolute inset-2 rounded-xl"
        style={{
          background: `radial-gradient(circle at center, ${colors.accent} 0%, ${colors.main} 30%, transparent 70%)`,
          opacity: 0.8,
          animation: "pulse 3s ease-in-out infinite",
          animationDelay: `${delay + 300}ms`,
        }}
      />
      
      {/* Radial rays effect */}
      <div
        className="absolute inset-0 rounded-2xl"
        style={{
          background: `conic-gradient(from 0deg at 50% 50%, transparent 0deg, ${colors.light} 45deg, transparent 90deg, ${colors.light} 135deg, transparent 180deg, ${colors.light} 225deg, transparent 270deg, ${colors.light} 315deg, transparent 360deg)`,
          opacity: 0.4,
          animation: "rotateGlow 8s linear infinite",
          animationDelay: `${delay}ms`,
        }}
      />
      
      {/* Inner highlight layer */}
      <div
        className="absolute inset-1 rounded-xl"
        style={{
          background: "linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 50%)",
          opacity: 0.6,
        }}
      />
      
      {/* Icon content with inner glow */}
      <div className="relative z-10 flex items-center justify-center h-full w-full">
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={{
            filter: `drop-shadow(0 0 8px ${colors.accent}) drop-shadow(0 0 4px ${colors.main})`,
          }}
        >
          <Icon className={`${iconSizes[size]} text-white`} strokeWidth={1.5} />
        </div>
      </div>
      
      {/* Bottom glow accent - like Resend */}
      <div
        className="absolute -bottom-3 left-1/2 -translate-x-1/2 w-3/4 h-2 rounded-full blur-lg"
        style={{
          background: `linear-gradient(to right, transparent, ${colors.accent}, transparent)`,
          opacity: 0.7,
          animation: "pulse 2s ease-in-out infinite",
          animationDelay: `${delay}ms`,
        }}
      />
      
      {/* Subtle top highlight */}
      <div
        className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-px"
        style={{
          background: "linear-gradient(to right, transparent, rgba(255, 255, 255, 0.3), transparent)",
        }}
      />
    </div>
  );
}

