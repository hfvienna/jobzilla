module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './data/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light"],
  },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
