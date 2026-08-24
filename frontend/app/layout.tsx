import type { Metadata } from "next";
import { Zilla_Slab, Inter, IBM_Plex_Mono } from "next/font/google";
import "./globals.css";

const slab = Zilla_Slab({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-slab",
  display: "swap",
});

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const mono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "TruthTrace AI | Chandigarh Police Digital Forensics",
  description: "AI-powered detection, verification, and origin tracing for manipulated media.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${slab.variable} ${sans.variable} ${mono.variable} font-sans bg-ink text-paper antialiased`}>
        {children}
      </body>
    </html>
  );
}
