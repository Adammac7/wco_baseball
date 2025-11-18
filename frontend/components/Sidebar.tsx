"use client";

import React, { useState } from "react";
import { BarChart2, Settings, Menu, User } from "lucide-react";


interface SidebarProps {
  items?: { name: string; icon?: React.ReactNode; link?: string }[];
}

const Sidebar: React.FC<SidebarProps> = ({ items }) => {
  const [open, setOpen] = useState(true);

  const defaultItems = [
    { name: "Leaderboard", icon: <BarChart2 size={18} />, link: "#" },
    { name: "By Player", icon: <User size={18} />, link: "#" },
    { name: "Settings", icon: <Settings size={18} />, link: "#" },
  ];

  const menuItems = items || defaultItems;

  return (
    <div
      className={`h-screen bg-gray-800 text-white p-4 transition-all duration-300 ${
        open ? "w-56" : "w-16"
      }`}
    >
      <div className="flex items-center justify-between mb-6">
        <h1 className={`text-lg font-semibold ${!open && "hidden"}`}>Players</h1>
        <button
          onClick={() => setOpen(!open)}
          className="text-gray-300 hover:text-white"
        >
          <Menu size={22} />
        </button>
      </div>

      <nav className="flex flex-col gap-2">
        {menuItems.map((item, index) => (
          <a
            key={index}
            href={item.link}
            className="flex items-center gap-3 px-2 py-2 rounded-md hover:bg-gray-700 transition"
          >
            {item.icon}
            {open && <span>{item.name}</span>}
          </a>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
