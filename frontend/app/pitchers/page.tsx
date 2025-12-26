"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpDown, TrendingUp, Zap, Target, BarChart3, Users } from "lucide-react";
import { AnimatedSection } from "@/components/AnimatedSection";

type SortField = "name" | "avgVelocity" | "maxVelocity" | "spinRate" | "era" | "games" | "so" | "bb" | null;
type SortDirection = "asc" | "desc";

interface Pitcher {
  name: string;
  team: string;
  avgVelocity: number;
  maxVelocity: number;
  spinRate: number;
  era: number;
  games: number;
  so: number;
  bb: number;
}

export default function PitchersPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortField, setSortField] = useState<SortField>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const pitchers: Pitcher[] = [
    { name: "Lettow, Rohan", team: "SDSU", avgVelocity: 89.2, maxVelocity: 92.9, spinRate: 2350, era: 0.00, games: 1, so: 0, bb: 0 },
    { name: "Shaw, Connor", team: "SDSU", avgVelocity: 80.1, maxVelocity: 84.4, spinRate: 1850, era: 0.00, games: 1, so: 0, bb: 0 },
  ];

  // Calculate quick stats
  const stats = useMemo(() => {
    const filtered = pitchers.filter((player) =>
      player.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    if (filtered.length === 0) return null;
    
    return {
      total: filtered.length,
      avgVelocity: filtered.reduce((sum, p) => sum + p.avgVelocity, 0) / filtered.length,
      maxVelocity: Math.max(...filtered.map(p => p.maxVelocity)),
      avgSpinRate: filtered.reduce((sum, p) => sum + p.spinRate, 0) / filtered.length,
      totalGames: filtered.reduce((sum, p) => sum + p.games, 0),
    };
  }, [searchQuery]);

  // Filter and sort
  const filteredAndSortedPitchers = useMemo(() => {
    let filtered = pitchers.filter((player) =>
      player.name.toLowerCase().includes(searchQuery.toLowerCase())
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

  const getVelocityColor = (velocity: number) => {
    if (velocity >= 90) return "text-green-400";
    if (velocity >= 85) return "text-yellow-400";
    return "text-gray-400";
  };

  const getEraColor = (era: number) => {
    if (era === 0) return "text-green-400";
    if (era <= 3.00) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <AnimatedSection direction="up" delay={0}>
          <div className="mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Pitchers</h1>
            <p className="text-gray-400 text-lg font-light">
              View and analyze pitcher performance statistics and metrics.
            </p>
          </div>
        </AnimatedSection>

        {/* Quick Stats Cards */}
        {stats && (
          <AnimatedSection direction="up" delay={100} threshold={0.1}>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Pitchers</span>
                <Users className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.total}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Avg Velocity</span>
                <Zap className="w-5 h-5 text-red-500" />
              </div>
              <p className={`relative z-10 text-3xl font-bold ${getVelocityColor(stats.avgVelocity)}`}>
                {stats.avgVelocity.toFixed(1)}<span className="text-lg text-gray-400"> mph</span>
              </p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Max Velocity</span>
                <TrendingUp className="w-5 h-5 text-red-500" />
              </div>
              <p className={`relative z-10 text-3xl font-bold ${getVelocityColor(stats.maxVelocity)}`}>
                {stats.maxVelocity.toFixed(1)}<span className="text-lg text-gray-400"> mph</span>
              </p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Avg Spin Rate</span>
                <BarChart3 className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">
                {Math.round(stats.avgSpinRate).toLocaleString()}<span className="text-lg text-gray-400"> rpm</span>
              </p>
            </div>
          </div>
          </AnimatedSection>
        )}

        {/* Search Bar */}
        <AnimatedSection direction="up" delay={200} threshold={0.1}>
          <div className="mb-8">
          <div className="relative max-w-md">
            <input
              type="text"
              placeholder="Search pitchers by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-gray-800 border border-gray-700 text-white placeholder-gray-400 rounded-xl focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-red-600 transition-all"
            />
            <svg
              className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
          </div>
        </AnimatedSection>

        {/* Pitchers Table */}
        <AnimatedSection direction="up" delay={300} threshold={0.1}>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-700 bg-gray-800 rounded-xl border border-gray-700 overflow-hidden shadow-lg">
            <thead className="bg-gradient-to-r from-red-950/50 via-red-900/30 to-gray-900 border-b border-red-800/50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("name")}
                    className={`flex items-center space-x-1 hover:text-white transition-colors ${
                      sortField === "name" ? "text-red-400" : ""
                    }`}
                  >
                    <span>Name</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-200 uppercase tracking-wider">Team</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("avgVelocity")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "avgVelocity" ? "text-red-400" : ""
                    }`}
                  >
                    <span>AVG VELOCITY</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("maxVelocity")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "maxVelocity" ? "text-red-400" : ""
                    }`}
                  >
                    <span>MAX VELOCITY</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("spinRate")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "spinRate" ? "text-red-400" : ""
                    }`}
                  >
                    <span>SPIN RATE</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("era")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "era" ? "text-red-400" : ""
                    }`}
                  >
                    <span>ERA</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("games")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "games" ? "text-red-400" : ""
                    }`}
                  >
                    <span>GAMES</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("so")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "so" ? "text-red-400" : ""
                    }`}
                  >
                    <span>SO</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("bb")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "bb" ? "text-red-400" : ""
                    }`}
                  >
                    <span>BB</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700 bg-gray-800">
              {filteredAndSortedPitchers.length > 0 ? (
                filteredAndSortedPitchers.map((player, index) => (
                  <tr
                    key={player.name}
                    className="hover:bg-gradient-to-r hover:from-red-950/20 hover:via-red-900/10 hover:to-transparent transition-all cursor-pointer group border-l-2 border-transparent hover:border-red-600/50"
                    onClick={() => router.push(`/pitchers/${player.name.replace(/\s+/g, '-').toLowerCase()}`)}
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white group-hover:text-red-400 transition-colors">
                      {player.name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{player.team}</td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getVelocityColor(player.avgVelocity)}`}>
                      {player.avgVelocity.toFixed(1)}<span className="text-gray-400"> mph</span>
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getVelocityColor(player.maxVelocity)}`}>
                      {player.maxVelocity.toFixed(1)}<span className="text-gray-400"> mph</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.spinRate.toLocaleString()}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${getEraColor(player.era)}`}>
                      {player.era.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{player.games}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{player.so}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{player.bb}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={9} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center">
                      <p className="text-gray-400 text-lg mb-2">
                        {searchQuery ? `No pitchers found matching "${searchQuery}"` : "No pitchers available"}
                      </p>
                      {searchQuery && (
                        <button
                          onClick={() => setSearchQuery("")}
                          className="text-red-600 hover:text-red-500 text-sm mt-2"
                        >
                          Clear search
                        </button>
                      )}
                    </div>
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
