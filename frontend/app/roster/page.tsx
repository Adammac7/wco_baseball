"use client";

import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpDown, Users, Target, BarChart3, Zap } from "lucide-react";
import { AnimatedSection } from "@/components/AnimatedSection";

type SortField = "name" | "position" | "games" | "avgVelocity" | "maxVelocity" | "avg" | "hits" | "hr" | "rbi" | null;
type SortDirection = "asc" | "desc";

interface Player {
  name: string;
  position: string;
  team: string;
  games: number;
  avgVelocity: number | null;
  maxVelocity: number | null;
  era: number | null;
  avg: number | null;
  hits: number | null;
  hr: number | null;
  rbi: number | null;
}

export default function RosterPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [positionFilter, setPositionFilter] = useState<string>("All");
  const [sortField, setSortField] = useState<SortField>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const positions = ["All", "Pitcher", "Hitter", "Catcher"];
  
  const players: Player[] = [
    { name: "Lettow, Rohan", position: "Pitcher", team: "SDSU", games: 1, avgVelocity: 89.2, maxVelocity: 92.9, era: 0.00, avg: null, hits: null, hr: null, rbi: null },
    { name: "Shaw, Connor", position: "Pitcher", team: "SDSU", games: 1, avgVelocity: 80.1, maxVelocity: 84.4, era: 0.00, avg: null, hits: null, hr: null, rbi: null },
    { name: "Jackson, Jake", position: "Hitter", team: "SDSU", games: 1, avgVelocity: null, maxVelocity: null, era: null, avg: 0.000, hits: 0, hr: 0, rbi: 0 },
    { name: "Farrell, Max", position: "Hitter", team: "SDSU", games: 1, avgVelocity: null, maxVelocity: null, era: null, avg: 0.000, hits: 0, hr: 0, rbi: 0 },
    { name: "Justice, Zach", position: "Hitter", team: "SDSU", games: 1, avgVelocity: null, maxVelocity: null, era: null, avg: 0.000, hits: 0, hr: 0, rbi: 0 },
    { name: "Trosky, Jabin", position: "Hitter", team: "SDSU", games: 1, avgVelocity: null, maxVelocity: null, era: null, avg: 1.000, hits: 1, hr: 0, rbi: 0 },
    { name: "Adams, Gage", position: "Catcher", team: "SDSU", games: 1, avgVelocity: null, maxVelocity: null, era: null, avg: 0.000, hits: 0, hr: 0, rbi: 0 },
  ];

  // Calculate quick stats
  const stats = useMemo(() => {
    const filtered = players.filter((player) => {
      const matchesSearch = player.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesPosition = positionFilter === "All" || player.position === positionFilter;
      return matchesSearch && matchesPosition;
    });
    
    if (filtered.length === 0) return null;
    
    const pitchers = filtered.filter(p => p.position === "Pitcher");
    const hitters = filtered.filter(p => p.position === "Hitter" || p.position === "Catcher");
    
    return {
      total: filtered.length,
      pitchers: pitchers.length,
      hitters: hitters.length,
      catchers: filtered.filter(p => p.position === "Catcher").length,
      totalGames: filtered.reduce((sum, p) => sum + p.games, 0),
    };
  }, [searchQuery, positionFilter]);

  // Filter and sort
  const filteredAndSortedPlayers = useMemo(() => {
    let filtered = players.filter((player) => {
      const matchesSearch = player.name.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesPosition = positionFilter === "All" || player.position === positionFilter;
      return matchesSearch && matchesPosition;
    });

    if (sortField) {
      filtered = [...filtered].sort((a, b) => {
        const aVal = a[sortField];
        const bVal = b[sortField];
        
        // Handle null values
        if (aVal === null && bVal === null) return 0;
        if (aVal === null) return 1;
        if (bVal === null) return -1;
        
        if (typeof aVal === "string") {
          return sortDirection === "asc"
            ? aVal.localeCompare(bVal as string)
            : (bVal as string).localeCompare(aVal);
        }
        return sortDirection === "asc" ? (aVal as number) - (bVal as number) : (bVal as number) - (aVal as number);
      });
    }

    return filtered;
  }, [searchQuery, positionFilter, sortField, sortDirection]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  const getDetailHref = (player: Player) => {
    if (player.position === "Pitcher") return `/pitchers/${player.name.replace(/\s+/g, '-').toLowerCase()}`;
    if (player.position === "Hitter") return `/hitters/${player.name.replace(/\s+/g, '-').toLowerCase()}`;
    return `/catchers/${player.name.replace(/\s+/g, '-').toLowerCase()}`;
  };

  const getPositionColor = (position: string) => {
    switch (position) {
      case "Pitcher": return "text-blue-400";
      case "Hitter": return "text-green-400";
      case "Catcher": return "text-yellow-400";
      default: return "text-gray-400";
    }
  };

  return (
    <div className="min-h-screen bg-black pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <AnimatedSection direction="up" delay={0}>
          <div className="mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">Roster</h1>
            <p className="text-gray-400 text-lg font-light">
              View the complete team roster and player information.
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
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Players</span>
                <Users className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.total}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Pitchers</span>
                <Zap className="w-5 h-5 text-blue-400" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-blue-400">{stats.pitchers}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Hitters</span>
                <Target className="w-5 h-5 text-green-400" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-green-400">{stats.hitters}</p>
            </div>
            <div className="relative bg-gradient-to-br from-red-900/30 via-red-800/20 to-gray-900 border border-red-800/50 rounded-xl p-6 shadow-lg hover:border-red-600 hover:shadow-red-600/20 transition-all overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-br from-red-600/0 to-red-600/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative z-10 flex items-center justify-between mb-2">
                <span className="text-gray-300 text-sm uppercase tracking-wide">Total Games</span>
                <BarChart3 className="w-5 h-5 text-red-500" />
              </div>
              <p className="relative z-10 text-3xl font-bold text-white">{stats.totalGames}</p>
            </div>
          </div>
          </AnimatedSection>
        )}

        {/* Search and Filter */}
        <AnimatedSection direction="up" delay={200} threshold={0.1}>
          <div className="mb-8 flex flex-col sm:flex-row gap-4">
            <div className="relative flex-1">
            <input
              type="text"
              placeholder="Search players by name..."
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
          <div className="flex gap-2 flex-wrap">
            {positions.map((position) => (
              <button
                key={position}
                onClick={() => setPositionFilter(position)}
                className={`px-6 py-3 rounded-xl font-medium transition-all ${
                  positionFilter === position
                    ? "bg-gradient-to-r from-red-600 to-red-700 text-white shadow-lg shadow-red-600/30 hover:from-red-700 hover:to-red-800"
                    : "bg-gray-800 text-gray-300 hover:bg-gradient-to-r hover:from-red-950/30 hover:to-gray-800 border border-gray-700 hover:border-red-800/50"
                }`}
              >
                {position}
              </button>
            ))}
          </div>
          </div>
        </AnimatedSection>

        {/* Roster Table */}
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
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-200 uppercase tracking-wider">
                  <button
                    onClick={() => handleSort("position")}
                    className={`flex items-center space-x-1 hover:text-white transition-colors ${
                      sortField === "position" ? "text-red-400" : ""
                    }`}
                  >
                    <span>Position</span>
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
                    <span>Games</span>
                    <ArrowUpDown className="w-4 h-4" />
                  </button>
                </th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">AVG VELOCITY</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">MAX VELOCITY</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">AVG</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">HITS</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">HR</th>
                <th className="px-6 py-4 text-right text-sm font-medium text-gray-200 uppercase tracking-wider">RBI</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700 bg-gray-800">
              {filteredAndSortedPlayers.length > 0 ? (
                filteredAndSortedPlayers.map((player, index) => (
                  <tr
                    key={player.name}
                    className="hover:bg-gradient-to-r hover:from-red-950/20 hover:via-red-900/10 hover:to-transparent transition-all cursor-pointer group border-l-2 border-transparent hover:border-red-600/50"
                    onClick={() => router.push(getDetailHref(player))}
                    style={{ animationDelay: `${index * 0.05}s` }}
                  >
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white group-hover:text-red-400 transition-colors">
                      {player.name}
                    </td>
                    <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${getPositionColor(player.position)}`}>
                      {player.position}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{player.team}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-400">{player.games}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.avgVelocity ? `${player.avgVelocity.toFixed(1)} mph` : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.maxVelocity ? `${player.maxVelocity.toFixed(1)} mph` : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.avg !== null ? player.avg.toFixed(3) : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.hits !== null ? player.hits : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.hr !== null ? player.hr : "-"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-white font-medium">
                      {player.rbi !== null ? player.rbi : "-"}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={10} className="px-6 py-12 text-center">
                    <div className="flex flex-col items-center">
                      <p className="text-gray-400 text-lg mb-2">
                        No players found{" "}
                        {searchQuery ? `matching "${searchQuery}"` : ""}
                        {positionFilter !== "All" ? `in position "${positionFilter}"` : ""}
                      </p>
                      {(searchQuery || positionFilter !== "All") && (
                        <button
                          onClick={() => {
                            setSearchQuery("");
                            setPositionFilter("All");
                          }}
                          className="text-red-600 hover:text-red-500 text-sm mt-2"
                        >
                          Clear filters
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

