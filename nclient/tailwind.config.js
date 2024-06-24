/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      height: {
        "app": "calc(100vh - 3rem)",
      },
      colors: {
        "app": {
          DEFAULT: "#495672",
          "dark": "#323b4e",
          "link": "#22847f",
        },
      }
    },
  },
  plugins: [],
};
