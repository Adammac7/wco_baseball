"use client";

import { ArrowRight, BarChart3, TrendingUp, Users, Target, Zap, Database, Shield, Activity, PlayCircle, Sparkles } from "lucide-react";
import Link from "next/link";
import { AnimatedSection } from "@/components/AnimatedSection";
import { AnimatedIcon } from "@/components/AnimatedIcon";

export default function HomePage() {
  const features = [
    {
      icon: BarChart3,
      title: "Advanced Analytics",
      description: "Real-time performance metrics and statistical analysis for every player",
      color: "red"
    },
    {
      icon: TrendingUp,
      title: "Performance Tracking",
      description: "Track velocity, spin rate, batting average, and more across all games",
      color: "blue"
    },
    {
      icon: Database,
      title: "Comprehensive Data",
      description: "198k+ data points from TrackMan technology, all in one place",
      color: "green"
    },
    {
      icon: Shield,
      title: "Data Accuracy",
      description: "100% accurate data processing with automated validation",
      color: "purple"
    },
    {
      icon: Activity,
      title: "Real-Time Updates",
      description: "Live statistics updated as games progress",
      color: "orange"
    },
    {
      icon: Target,
      title: "Player Insights",
      description: "Deep dive into individual player performance and trends",
      color: "pink"
    }
  ];

  const capabilities = [
    {
      title: "Hitter Analysis",
      description: "Comprehensive batting statistics including AVG, OBP, SLG, and OPS",
      stats: ["AVG", "OBP", "SLG", "OPS", "PA"]
    },
    {
      title: "Pitcher Metrics",
      description: "Velocity tracking, spin rate analysis, and ERA calculations",
      stats: ["Velocity", "Spin Rate", "ERA", "SO", "BB"]
    },
    {
      title: "Catcher Performance",
      description: "Pop time, throw speed, and defensive statistics",
      stats: ["Pop Time", "Throw Speed", "Games", "AB"]
    }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section */}
      <div className="relative pt-20 pb-16 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center min-h-[80vh]">
            
            {/* Left Side - Content */}
            <div className="flex flex-col justify-center space-y-8 z-10">
              <div className="space-y-6">
                <AnimatedSection direction="left" delay={0}>
                  <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight">
                    Baseball Data
                    <br />
                    <span className="text-red-600 animate-fade-in-scale animate-delay-200">Platform</span>
                  </h1>
                </AnimatedSection>
                
                <AnimatedSection direction="left" delay={300}>
                  <p className="text-xl md:text-2xl text-gray-300 font-light leading-relaxed max-w-xl">
                    Advanced analytics and performance tracking for the{" "}
                    <span className="text-red-600 font-medium">San Diego State University</span> baseball program.
                  </p>
                </AnimatedSection>
                
                <AnimatedSection direction="left" delay={500}>
                  <p className="text-lg text-gray-400 leading-relaxed max-w-xl">
                    Track player statistics, analyze performance metrics, and make data-driven decisions.
                  </p>
                </AnimatedSection>
              </div>

              {/* CTA Buttons */}
              <AnimatedSection direction="left" delay={700}>
                <div className="flex flex-col sm:flex-row gap-4 pt-4">
                  <Link
                    href="/roster"
                    className="group inline-flex items-center justify-center px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105 shadow-lg shadow-red-600/20"
                  >
                    View Roster
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Link>
                  <Link
                    href="/hitters"
                    className="group inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-gray-700 hover:border-gray-600 text-white font-semibold rounded-lg transition-all"
                  >
                    Explore Stats
                    <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                  </Link>
                </div>
              </AnimatedSection>
            </div>

            {/* Right Side - Animated Graphic */}
            <AnimatedSection direction="right" delay={300}>
              <div className="relative flex items-center justify-center lg:justify-end h-[400px] lg:h-[600px]">
                <div className="relative w-full max-w-lg h-full">
                {/* Background Grid */}
                <div className="absolute inset-0 opacity-10">
                  <div className="grid grid-cols-10 gap-1 h-full w-full">
                    {Array.from({ length: 100 }).map((_, i) => (
                      <div
                        key={i}
                        className="bg-gray-700 rounded-sm animate-pulse"
                        style={{
                          animationDelay: `${(i % 10) * 0.1}s`,
                          animationDuration: '2s',
                        }}
                      />
                    ))}
                  </div>
                </div>

                {/* Central Baseball Diamond */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="relative">
                    {/* Outer Ring */}
                    <div className="absolute inset-0 border-4 border-red-600/30 rounded-full animate-pulse" style={{ width: '200px', height: '200px', margin: '-100px' }} />
                    
                    {/* Middle Ring */}
                    <div className="absolute inset-0 border-4 border-red-600/50 rounded-full animate-pulse" style={{ width: '150px', height: '150px', margin: '-75px', animationDelay: '0.5s' }} />
                    
                    {/* Inner Core */}
                    <div className="relative w-24 h-24 bg-gradient-to-br from-red-600 to-red-800 rounded-full flex items-center justify-center shadow-2xl shadow-red-600/50">
                      <div className="text-white font-bold text-2xl">SD</div>
                    </div>

                    {/* Floating Stats Nodes */}
                    {[
                      { top: '-20%', left: '50%', label: 'AVG', value: '.312' },
                      { top: '50%', left: '-20%', label: 'VEL', value: '92' },
                      { top: '50%', left: '120%', label: 'ERA', value: '0.00' },
                      { top: '120%', left: '50%', label: 'OPS', value: '.916' },
                    ].map((node, i) => (
                      <div
                        key={i}
                        className="absolute bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-lg transform -translate-x-1/2 -translate-y-1/2 animate-float"
                        style={{
                          top: node.top,
                          left: node.left,
                          animationDelay: `${i * 0.2}s`,
                        }}
                      >
                        <div className="text-xs text-gray-400 uppercase mb-1">{node.label}</div>
                        <div className="text-lg font-bold text-white">{node.value}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Floating Particles */}
                {Array.from({ length: 20 }).map((_, i) => (
                  <div
                    key={i}
                    className="absolute w-2 h-2 bg-red-600/30 rounded-full animate-float"
                    style={{
                      top: `${Math.random() * 100}%`,
                      left: `${Math.random() * 100}%`,
                      animationDelay: `${Math.random() * 2}s`,
                      animationDuration: `${3 + Math.random() * 2}s`,
                    }}
                  />
                ))}
                </div>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <AnimatedSection direction="up" delay={0} threshold={0.2}>
        <div className="bg-black py-20 px-4 sm:px-6 lg:px-8 border-t border-gray-800">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <AnimatedSection direction="down" delay={0}>
                <AnimatedIcon icon={Sparkles} delay={0} glowColor="red" size="md" />
              </AnimatedSection>
              <AnimatedSection direction="down" delay={200}>
                <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                  Powerful <span className="text-red-600">Features</span>
                </h2>
              </AnimatedSection>
              <AnimatedSection direction="down" delay={400}>
                <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                  Everything you need to analyze and improve player performance
                </p>
              </AnimatedSection>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => {
                const Icon = feature.icon;
                return (
                  <AnimatedSection
                    key={index}
                    direction="scale"
                    delay={index * 100}
                    threshold={0.1}
                  >
                    <div className="group bg-gray-900 border border-gray-800 rounded-xl p-6 transition-all duration-300 hover:border-red-600 hover:transform hover:-translate-y-2 hover:shadow-xl hover:shadow-red-600/10">
                      <div className="mb-4">
                        <div className="w-12 h-12 bg-red-600/10 rounded-lg flex items-center justify-center group-hover:bg-red-600/20 transition-colors">
                          <Icon className="w-6 h-6 text-red-600" />
                        </div>
                      </div>
                      <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                      <p className="text-gray-400 text-sm leading-relaxed">{feature.description}</p>
                    </div>
                  </AnimatedSection>
                );
              })}
            </div>
          </div>
        </div>
      </AnimatedSection>

      {/* Capabilities Section */}
      <AnimatedSection direction="up" delay={0} threshold={0.2}>
        <div className="bg-black py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-16">
              <AnimatedSection direction="down" delay={0}>
                <AnimatedIcon icon={BarChart3} delay={0} glowColor="blue" size="md" />
              </AnimatedSection>
              <AnimatedSection direction="down" delay={200}>
                <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
                  Comprehensive <span className="text-red-600">Analysis</span>
                </h2>
              </AnimatedSection>
              <AnimatedSection direction="down" delay={400}>
                <p className="text-xl text-gray-400 max-w-2xl mx-auto">
                  Track every aspect of player performance with precision
                </p>
              </AnimatedSection>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {capabilities.map((capability, index) => (
                <AnimatedSection
                  key={index}
                  direction={index % 2 === 0 ? "left" : "right"}
                  delay={index * 150}
                  threshold={0.1}
                >
                  <div className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700 rounded-xl p-8 transition-all duration-300 hover:border-red-600 hover:transform hover:-translate-y-2 hover:shadow-xl hover:shadow-red-600/10">
                    <h3 className="text-2xl font-bold text-white mb-3">{capability.title}</h3>
                    <p className="text-gray-400 mb-6">{capability.description}</p>
                    <div className="flex flex-wrap gap-2">
                      {capability.stats.map((stat, i) => (
                        <span
                          key={i}
                          className="px-3 py-1 bg-red-600/10 border border-red-600/20 rounded-lg text-sm text-red-600 font-medium animate-fade-in-scale"
                          style={{ animationDelay: `${(index * 150 + i * 50)}ms` }}
                        >
                          {stat}
                        </span>
                      ))}
                    </div>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </div>
      </AnimatedSection>

      {/* Stats Section */}
      <AnimatedSection direction="up" delay={0} threshold={0.2}>
        <div className="bg-black py-16 px-4 sm:px-6 lg:px-8 border-t border-gray-800">
          <div className="max-w-7xl mx-auto">
            <div className="text-center mb-12">
              <AnimatedSection direction="down" delay={0}>
                <AnimatedIcon icon={Database} delay={0} glowColor="purple" size="md" />
              </AnimatedSection>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[
                { value: "7", label: "Players Tracked" },
                { value: "198k+", label: "Data Points" },
                { value: "100%", label: "Data Accuracy" },
              ].map((stat, index) => (
                <AnimatedSection
                  key={index}
                  direction="scale"
                  delay={index * 150}
                  threshold={0.1}
                >
                  <div className="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-800 rounded-xl p-8 transition-all hover:border-red-600 hover:transform hover:-translate-y-1 text-center">
                    <div className="text-5xl font-bold text-white mb-2">{stat.value}</div>
                    <div className="text-gray-400 text-lg">{stat.label}</div>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </div>
      </AnimatedSection>

      {/* CTA Section */}
      <AnimatedSection direction="up" delay={0} threshold={0.2}>
        <div className="bg-gradient-to-br from-gray-900 to-black py-20 px-4 sm:px-6 lg:px-8 border-t border-gray-800">
          <div className="max-w-4xl mx-auto text-center">
            <AnimatedSection direction="down" delay={0}>
              <AnimatedIcon icon={PlayCircle} delay={0} glowColor="orange" size="lg" />
            </AnimatedSection>
            <AnimatedSection direction="down" delay={200}>
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                Ready to <span className="text-red-600">Explore</span> the Data?
              </h2>
            </AnimatedSection>
            <AnimatedSection direction="down" delay={400}>
              <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
                Start analyzing player performance and make data-driven decisions for your team
              </p>
            </AnimatedSection>
            <AnimatedSection direction="up" delay={600}>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/roster"
                  className="group inline-flex items-center justify-center px-8 py-4 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition-all transform hover:scale-105 shadow-lg shadow-red-600/20"
                >
                  View Full Roster
                  <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Link>
                <Link
                  href="/hitters"
                  className="group inline-flex items-center justify-center px-8 py-4 bg-transparent border-2 border-gray-700 hover:border-gray-600 text-white font-semibold rounded-lg transition-all"
                >
                  View Analytics
                  <PlayCircle className="ml-2 w-5 h-5 group-hover:scale-110 transition-transform" />
                </Link>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </AnimatedSection>
    </div>
  );
}
