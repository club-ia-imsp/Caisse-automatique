/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#16881c',
          dark: '#1f8227',
          600: '#16881c',
          700: '#1f8227',
        },
        secondary: {
          DEFAULT: '#62a168',
          light: '#78bf79',
          dark: '#459c4a',
          400: '#78bf79',
          500: '#62a168',
          600: '#459c4a',
        },
        surface: {
          DEFAULT: '#dedfde',
          light: '#f5f6f5',
          border: '#b7d7b8',
          muted: '#c4d9c5',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
