"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { Menu, X, Home,BarChart3,Users } from "lucide-react";
import { useState } from "react";

export function Navbar() {
 const pathname = usePathname();
 const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

 const navItems = [
  { href: "/", label: "Home", icon: Home },
  { href: "/hitters", label: "Hitters", icon: BarChart3 },
  { href: "/pitchers", label: "Pitchers", icon: BarChart3 },
  { href: "/catchers", label: "Catchers", icon: BarChart3 },
  { href: "/roster", label: "Roster", icon: Users }
 ];

 return (
  <header
    className="
      fixed top-4 left-1/2 -translate-x-1/2 z-50
      backdrop-blur-[5px]
      shadow-[0_0_30px_rgba(227,228,237,0.37)]
      border border-gray-400/40
      rounded-[30px]
      w-[60%]
      flex justify-center
    "
  >
    <div className="w-full px-4 sm:px-6 lg:px-8">
      <div className="flex justify-center items-center h-16">

        <nav className="hidden lg:flex items-center space-x-8">
          <Link href="/" className="navbar-logo flex items-center">
            <Image 
              src="/SDSU_logo.webp" 
              alt="SDSU Aztec Baseball Logo" 
              width={40}
              height={40}
              className="h-10 w-auto" 
            />
            <span className="ml-3 text-xl font-bold text-white transition-colors hidden sm:block">
              SDSU Aztec Baseball
            </span>
          </Link>

          {navItems.map(({ href, label, icon: Icon }) => (
  <Link
    key={href}
    href={href}
    className={`
      group relative flex items-center space-x-2 text-sm font-medium text-white
      ${pathname === href ? "opacity-100" : "opacity-80 hover:opacity-100"}
    `}
  >
    <Icon className="h-5 w-5" />
    <span>{label}</span>

    {/* underline */}
    <span
      className={`
        absolute left-0 -bottom-1 h-0.5 bg-red-500 transition-all duration-300
        ${pathname === href ? "w-full" : "w-0 group-hover:w-full"}
      `}
    />
  </Link>
))}

        </nav>

      </div>
    </div>

    {/* Mobile Menu */}
    <div
      className={`mobile-menu lg:hidden transition-all duration-300 ease-in-out overflow-hidden ${
        isMobileMenuOpen ? "max-h-screen opacity-100 py-2" : "max-h-0 opacity-0"
      }`}
    >
      <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            onClick={() => setIsMobileMenuOpen(false)}
            className={`navbar-link flex items-center space-x-3 text-base font-medium text-white ${
              pathname === href ? "active" : "hover:opacity-80"
            }`}
          >
            <Icon className="h-5 w-5" />
            <span>{label}</span>
          </Link>
        ))}
      </div>
    </div>
  </header>
);

}