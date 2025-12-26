"use client";

import { useState, useEffect, useRef } from "react";
import { Search, X, Loader2 } from "lucide-react";

interface EnhancedSearchProps {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  onClear?: () => void;
  debounceMs?: number;
  showResultsCount?: boolean;
  resultsCount?: number;
  className?: string;
}

export function EnhancedSearch({
  placeholder = "Search...",
  value,
  onChange,
  onClear,
  debounceMs = 300,
  showResultsCount = false,
  resultsCount,
  className = "",
}: EnhancedSearchProps) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  const [isSearching, setIsSearching] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Debounce search
  useEffect(() => {
    setIsSearching(true);
    const timer = setTimeout(() => {
      setDebouncedValue(value);
      setIsSearching(false);
      onChange(value);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [value, debounceMs, onChange]);

  // Keyboard shortcut: Cmd/Ctrl + K to focus search
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleClear = () => {
    onChange("");
    onClear?.();
    inputRef.current?.focus();
  };

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500 pointer-events-none" />
        <input
          ref={inputRef}
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full pl-12 pr-20 py-3 bg-gray-800 border border-gray-700 text-white placeholder-gray-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-red-600 transition-all"
        />
        <div className="absolute right-4 top-1/2 transform -translate-y-1/2 flex items-center gap-2">
          {isSearching && value && (
            <Loader2 className="w-4 h-4 text-gray-500 animate-spin" />
          )}
          {value && !isSearching && (
            <button
              onClick={handleClear}
              className="p-1 text-gray-500 hover:text-white transition-colors rounded-full hover:bg-gray-700"
              aria-label="Clear search"
            >
              <X className="w-4 h-4" />
            </button>
          )}
          {!value && (
            <kbd className="hidden sm:inline-flex px-2 py-1 text-xs font-semibold text-gray-500 bg-gray-900 border border-gray-700 rounded">
              ⌘K
            </kbd>
          )}
        </div>
      </div>
      {showResultsCount && resultsCount !== undefined && value && (
        <div className="mt-2 text-sm text-gray-400 animate-fade-in-up">
          {resultsCount} {resultsCount === 1 ? "result" : "results"} found
        </div>
      )}
    </div>
  );
}

