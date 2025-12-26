"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpDown, Target, BarChart3, Users, TrendingUp } from "lucide-react";
import { AnimatedSection } from "@/components/AnimatedSection";

type SortField = "name" | "games" | "ab" | "hits" | "hr" | "rbi" | null;
type SortDirection = "asc" | "desc";

interface Catcher {
  name: string;
  team: string;
  games: number;
  ab: number;
  hits: number;
  hr: number;
  rbi: number;
}

export default function CatchersPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [sortField, setSortField] = useState<SortField>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const catchers: Catcher[] = [
    { name: "Adams, Gage", team: "SDSU", games: 1, ab: 0, hits: 0, hr: 0, rbi: 0 },
  ];

  // Calculate quick stats
  const stats = useMemo(() => {
    const filtered = catchers.filter((player) =>
      player.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    if (filtered.length === 0) return null;
    
    const totalAb = filtered.reduce((sum, c) => sum + c.ab, 0);
    const totalHits = filtered.reduce((sum, c) => sum + c.hits, 0);
    
    return {
      total: filtered.length,
      totalGames: filtered.reduce((sum, c) => sum + c.games, 0),
      totalAb: totalAb,
      totalHits: totalHits,
      avg: totalAb > 0 ? totalHits / totalAb : 0,
      totalHr: filtered.reduce((sum, c) => sum + c.hr, 0),
      totalRbi: filtered.reduce((sum, c) => sum + c.rbi, 0),
    };
  }, [searchQuery]);

  // Filter and sort
  const filteredAndSortedCatchers = useMemo(() => {
    let filtered = catchers.filter((player) =>
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

  const formatAvg = (avg: number) => {
    if (avg === 0) return ".000";
    return avg.toFixed(3).replace(/^0+/, "");
  };

  const getAvgColor = (avg: number) => {
    if (avg >= 0.300) return "text-green-400";
    if (avg >= 0.250) return "text-yellow-400";
    return "text-gray-400";
  };

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <AnimatedSection direction="up" delay={0}>
          <div className="mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Catchers</h1>
            <p className="text-gray-400 text-lg font-light">
              View and analyze catcher performance statistics and metrics.
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
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Catchers</span>
                <Users className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.total}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Batting Avg</span>
                <Target className="w-5 h-5 text-red-500" />
              </div>
              <p className={`relative z-10 text-3xl font-bold ${getAvgColor(stats.avg)}`}>
                {formatAvg(stats.avg)}
              </p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Hits</span>
                <TrendingUp className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.totalHits}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total RBI</span>
                <BarChart3 className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.totalRbi}</p>
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
              placeholder="Search catchers by name..."
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

        {/* Catchers Table */}
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
                    onClick={() => handleSort("ab")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "ab" ? "text-red-400" : ""
                    }`}
                  >
                    <span>AB</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("hits")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "hits" ? "text-red-400" : ""
                    }`}
                  >
                    <span>HITS</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("hr")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "hr" ? "text-red-400" : ""
                    }`}
                  >
                    <span>HR</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("rbi")}
                    className={`flex items-center space-x-1 ml-auto hover:text-white transition-colors ${
                      sortField === "rbi" ? "text-red-400" : ""
                    }`}
                  >
                    <span>RBI</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700 bg-gray-800">
              {filteredAndSortedCatchers.length > 0 ? (
                filteredAndSortedCatchers.map((player, index) => {
                  const avg = player.ab > 0 ? player.hits / player.ab : 0;
                  return (
                    <tr
                      key={player.name}
                      className="hover:bg-gradient-to-r hover:from-red-950/20 hover:via-red-900/10 hover:to-transparent transition-all cursor-pointer group border-l-2 border-transparent hover:border-red-600/50"
                      onClick={() => router.push(`/catchers/${player.name.replace(/\s+/g, '-').toLowerCase()}`)}
                      style={{ animationDelay: `${index * 0.05}s` }}
                    >
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white group-hover:text-red-400 transition-colors">
                        {player.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{player.team}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{player.games}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">{player.ab}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">{player.hits}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">{player.hr}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">{player.rbi}</td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center">
                      <p className="text-gray-400 text-lg mb-2">
                        {searchQuery ? `No catchers found matching "${searchQuery}"` : "No catchers available"}
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
