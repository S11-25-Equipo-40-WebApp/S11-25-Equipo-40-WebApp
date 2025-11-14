import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: "class",
  content: [
    "./src/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
    colors: {
    border: "var(--border)",
    background: "var(--background)",
    foreground: "var(--foreground)",
    }

    },
  },
  plugins: [],
}

export default config
