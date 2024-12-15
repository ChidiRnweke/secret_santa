/** @type {import('tailwindcss').Config} */
import primeUIPlugin from 'tailwindcss-primeui'
export default {
  darkMode: 'selector',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'secret-santa': "url('/christmas.svg')",
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'], // Sets Roboto as the default sans-serif
      },
    },
  },
  plugins: [primeUIPlugin],
}
