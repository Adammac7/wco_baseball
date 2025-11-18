import type { Metadata } from "next";
import { Navbar } from "@/components/navbar";
import "./globals.css";


export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="relative min-h-screen flex flex-col items-center justify-center pt-20 bg-gray-900"
      style={{
        backgroundImage: `url('/aztec_cal.jpg')`,
        backgroundSize: "cover",
        backgroundPosition: "top",
      }}>
        <Navbar />
        {children}
      </body>
    </html>
  );
}

