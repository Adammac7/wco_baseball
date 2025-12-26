"use client";

import { useState, useMemo } from "react";
import { ArrowUpDown, TrendingUp, Target, BarChart3, Users, Info } from "lucide-react";
import { EnhancedSearch } from "@/components/EnhancedSearch";
import { EmptyState } from "@/components/EmptyState";
import { ExportButton } from "@/components/ExportButton";
import { Tooltip } from "@/components/Tooltip";
import { useKeyboardShortcuts } from "@/components/KeyboardShortcut";
import { AnimatedSection } from "@/components/AnimatedSection";

type SortField = "name" | "avg" | "obp" | "slg" | "ops" | "pa" | null;
type SortDirection = "asc" | "desc";

interface Hitter {
  name: string;
  team: string;
  avg: number;
  obp: number;
  slg: number;
  ops: number;
  pa: number;
}

export default function HittersPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortField, setSortField] = useState<SortField>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");
  
  // Keyboard shortcuts
  useKeyboardShortcuts([
    {
      key: "f",
      ctrl: true,
      action: () => {
        const searchInput = document.querySelector('input[type="text"]') as HTMLInputElement;
        searchInput?.focus();
      },
      description: "Focus search",
    },
  ]);
  
  const hitters: Hitter[] = [
    { name: "John Doe", team: "SDSU", avg: 0.312, obp: 0.395, slg: 0.521, ops: 0.916, pa: 412 },
    { name: "Alex Smith", team: "SDSU", avg: 0.287, obp: 0.356, slg: 0.468, ops: 0.824, pa: 389 },
    { name: "Sam Lee", team: "SDSU", avg: 0.265, obp: 0.338, slg: 0.402, ops: 0.740, pa: 350 },
  ];

  // Calculate quick stats
  const stats = useMemo(() => {
    const filtered = hitters.filter((hitter) =>
      hitter.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    if (filtered.length === 0) return null;
    
    return {
      total: filtered.length,
      avgAvg: filtered.reduce((sum, h) => sum + h.avg, 0) / filtered.length,
      avgOps: filtered.reduce((sum, h) => sum + h.ops, 0) / filtered.length,
      totalPa: filtered.reduce((sum, h) => sum + h.pa, 0),
    };
  }, [searchQuery]);

  // Filter and sort
  const filteredAndSortedHitters = useMemo(() => {
    let filtered = hitters.filter((hitter) =>
      hitter.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (sortField) {
      filtered = [...filtered].sort((a, b) => {
        const aVal = a[sortField];
        const bVal = b[sortField];
        if (typeof aVal === "string") {
          return sortDirection === "asc"
            ? aVal.localeCompare(bVal as string)
            : (bVal as string).localeCompare(aVal);
        }
        return sortDirection === "asc" ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number);
      });
    }

    return filtered;
  }, [searchQuery, sortField, sortDirection]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  const formatStat = (value: number, decimals: number = 3) => {
    return value.toFixed(decimals).replace(/^0+/, "");
  };

  const getStatColor = (value: number, type: "avg" | "ops") => {
    if (type === "avg") {
      if (value >= 0.300) return "text-green-400";
      if (value >= 0.250) return "text-yellow-400";
      return "text-gray-400";
    } else {
      if (value >= 0.800) return "text-green-400";
      if (value >= 0.700) return "text-yellow-400";
      return "text-gray-400";
    }
  };

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <AnimatedSection direction="up" delay={0}>
          <div className="mb-12">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-5xl font-bold text-white mb-2">Hitters</h1>
                <p className="text-gray-400 text-lg font-light">
                  View and analyze hitter performance statistics and metrics.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <Tooltip content="Press ⌘K to focus search, ⌘E to export">
                  <button className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-all">
                    <Info className="w-5 h-5" />
                  </button>
                </Tooltip>
                <ExportButton
                  data={filteredAndSortedHitters.map((h) => ({
                    Name: h.name,
                    Team: h.team,
                    AVG: h.avg.toFixed(3),
                    OBP: h.obp.toFixed(3),
                    SLG: h.slg.toFixed(3),
                    OPS: h.ops.toFixed(3),
                    PA: h.pa,
                  }))}
                  filename="hitters"
                />
              </div>
            </div>
          </div>
        </AnimatedSection>

        {/* Quick Stats Cards */}
        {stats && (
          <AnimatedSection direction="up" delay={100} threshold={0.1}>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Hitters</span>
                <Users className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.total}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Avg AVG</span>
                <Target className="w-5 h-5 text-red-500" />
              </div>
              <p className={`relative z-10 text-3xl font-bold ${getStatColor(stats.avgAvg, "avg")}`}>
                {formatStat(stats.avgAvg)}
              </p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Avg OPS</span>
                <TrendingUp className="w-5 h-5 text-red-500" />
              </div>
              <p className={`relative z-10 text-3xl font-bold ${getStatColor(stats.avgOps, "ops")}`}>
                {formatStat(stats.avgOps)}
              </p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total PA</span>
                <BarChart3 className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.totalPa.toLocaleString()}</p>
            </div>
          </div>
          </AnimatedSection>
        )}

        {/* Search Bar */}
        <AnimatedSection direction="up" delay={200} threshold={0.1}>
          <div className="mb-8">
            <EnhancedSearch
            placeholder="Search hitters by name..."
            value={searchQuery}
            onChange={setSearchQuery}
            onClear={() => setSearchQuery("")}
            showResultsCount={true}
            resultsCount={filteredAndSortedHitters.length}
            className="max-w-md"
          />
          </div>
        </AnimatedSection>

        {/* Hitters Table */}
        <AnimatedSection direction="up" delay={300} threshold={0.1}>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-700 bg-gray-800 rounded-xl border border-gray-700 overflow-hidden shadow-lg">
            <thead className="bg-gradient-to-r from-red-950/50 via-red-900/30 to-gray-900 border-b border-red-800/50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="Click to sort by name">
                    <button
                      onClick={() => handleSort("name")}
                      className={`flex items-center space-x-1 hover:text-white transition-colors ${
                        sortField === "name" ? "text-red-400" : ""
                      }`}
                    >
                      <span>Name</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="Team name">Team</Tooltip>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="Batting Average - Click to sort">
                    <button
                      onClick={() => handleSort("avg")}
                      className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                        sortField === "avg" ? "text-red-400" : ""
                      }`}
                    >
                      <span>AVG</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="On-Base Percentage - Click to sort">
                    <button
                      onClick={() => handleSort("obp")}
                      className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                        sortField === "obp" ? "text-red-400" : ""
                      }`}
                    >
                      <span>OBP</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="Slugging Percentage - Click to sort">
                    <button
                      onClick={() => handleSort("slg")}
                      className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                        sortField === "slg" ? "text-red-400" : ""
                      }`}
                    >
                      <span>SLG</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="On-Base Plus Slugging - Click to sort">
                    <button
                      onClick={() => handleSort("ops")}
                      className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                        sortField === "ops" ? "text-red-400" : ""
                      }`}
                    >
                      <span>OPS</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <Tooltip content="Plate Appearances - Click to sort">
                    <button
                      onClick={() => handleSort("pa")}
                      className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                        sortField === "pa" ? "text-red-400" : ""
                      }`}
                    >
                      <span>PA</span>
                      <ArrowUpDown className="w-4 h-4" />
                    </button>
                  </Tooltip>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700 bg-gray-800">
              {filteredAndSortedHitters.length > 0 ? (
                filteredAndSortedHitters.map((hitter, index) => (
                  <tr
                    key={hitter.name}
                    className="hover:bg-gradient-to-r hover:from-red-950/20 hover:via-red-900/10 hover:to-transparent transition-all cursor-pointer group border-l-2 border-transparent hover:border-red-600/50"
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white group-hover:text-red-400 transition-colors">
                      {hitter.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{hitter.team}</td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getStatColor(hitter.avg, "avg")}`}>
                      {formatStat(hitter.avg)}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getStatColor(hitter.obp, "avg")}`}>
                      {formatStat(hitter.obp)}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getStatColor(hitter.slg, "avg")}`}>
                      {formatStat(hitter.slg)}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getStatColor(hitter.ops, "ops")}`}>
                      {formatStat(hitter.ops)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{hitter.pa.toLocaleString()}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="px-6 py-12">
                    <EmptyState
                      type={searchQuery ? "search" : "default"}
                      title={searchQuery ? "No hitters found" : "No hitters available"}
                      description={
                        searchQuery
                          ? `No hitters match "${searchQuery}". Try adjusting your search terms.`
                          : "There are currently no hitters in the database."
                      }
                      action={
                        searchQuery ? (
                          <button
                            onClick={() => setSearchQuery("")}
                            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-all"
                          >
                            Clear search
                          </button>
                        ) : undefined
                      }
                    />
                  </td>
                </tr>
              )}
            </tbody>
          </table>
          </div>
        </AnimatedSection>
      </div>
    </div>
  );
}
