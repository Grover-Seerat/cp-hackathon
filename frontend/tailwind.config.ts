import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#0a0e14",       // near-black navy background
        surface: "#121822",    // panel background
        surface2: "#182131",   // raised panel background
        hairline: "#232d3d",   // borders / dividers
        muted: "#7c8797",      // secondary text
        paper: "#e7ecf3",      // primary text
        stamp: "#c9962c",      // amber stamp ink — case IDs, active states
        danger: "#c1443a",     // manipulated / fake verdict
        safe: "#3f9c6d",       // authentic verdict
      },
      fontFamily: {
        display: ["var(--font-slab)", "serif"],
        sans: ["var(--font-sans)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      backgroundImage: {
        "grain": "radial-gradient(circle at 1px 1px, rgba(231,236,243,0.035) 1px, transparent 0)",
      },
      backgroundSize: {
        "grain": "24px 24px",
      },
    },
  },
  plugins: [],
};

export default config;
