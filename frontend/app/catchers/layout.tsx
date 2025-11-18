import type { Metadata } from "next";
import "../globals.css";

export default function HittersLayout({ children }: { children: React.ReactNode }) {
  // This is a nested layout — do NOT include <html> or <body> here.
  // The root `app/layout.tsx` provides the page shell (html/body and Navbar).
  return <>{children}</>;
}