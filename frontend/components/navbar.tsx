"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { Menu, X, Home, BarChart3, Users } from "lucide-react";
import { useState, useEffect, useMemo } from "react";

export function Navbar() {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [activePath, setActivePath] = useState(pathname);

  // Update active path immediately when pathname changes
  useEffect(() => {
    setActivePath(pathname);
  }, [pathname]);

  // Memoize navItems to avoid recreating on every render
  const navItems = useMemo(() => [
    { href: "/", label: "Home", icon: Home },
    { href: "/hitters", label: "Hitters", icon: BarChart3 },
    { href: "/pitchers", label: "Pitchers", icon: BarChart3 },
    { href: "/catchers", label: "Catchers", icon: BarChart3 },
    { href: "/roster", label: "Roster", icon: Users }
  ], []);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-black/95 backdrop-blur-sm border-b border-gray-800 shadow-lg">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand/Logo */}
          <Link href="/" className="flex items-center space-x-3 hover:opacity-90 transition-opacity group">
            <div className="relative">
              <Image 
                src="/SDSU_logo.webp" 
                alt="SDSU Aztec Baseball Logo" 
                width={45}
                height={45}
                className="h-11 w-auto transition-transform group-hover:scale-105" 
              />
            </div>
            <span className="text-xl font-bold text-white hidden sm:block tracking-tight">
              SDSU <span className="text-red-600">Aztecs</span> Baseball
            </span>
          </Link>
          
          {/* Desktop Navigation Links */}
          <nav className="hidden lg:flex items-center space-x-2">
            {navItems.map(({ href, label, icon: Icon }) => {
              // Handle active state: exact match for home, startsWith for other routes
              const isActive = href === "/" 
                ? activePath === "/"
                : activePath.startsWith(href);
              return (
                <Link
                  key={href}
                  href={href}
                  onClick={() => setActivePath(href)}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-50 ${
                    isActive
                      ? "bg-red-600 text-white shadow-lg shadow-red-600/20"
                      : "text-gray-300 hover:text-white hover:bg-gray-800/50"
                  }`}
                  style={{ willChange: 'background-color' }}
                >
                  <Icon className="h-4 w-4" />
                  <span>{label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden p-2 text-gray-300 hover:text-white rounded-md focus:outline-none focus:ring-2 focus:ring-red-600"
            aria-expanded={isMobileMenuOpen ? "true" : "false"}
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Panel */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-gray-900/95 backdrop-blur-sm border-t border-gray-800 shadow-lg">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navItems.map(({ href, label, icon: Icon }) => {
              // Handle active state: exact match for home, startsWith for other routes
              const isActive = href === "/" 
                ? activePath === "/"
                : activePath.startsWith(href);
              return (
                <Link
                  key={href}
                  href={href}
                  onClick={() => {
                    setActivePath(href);
                    setIsMobileMenuOpen(false);
                  }}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-base font-medium transition-colors duration-50 ${
                    isActive
                      ? "bg-red-600 text-white shadow-lg shadow-red-600/20"
                      : "text-gray-300 hover:text-white hover:bg-gray-800/50"
                  }`}
                  style={{ willChange: 'background-color' }}
                >
                  <Icon className="h-5 w-5" />
                  <span>{label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
