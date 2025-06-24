/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        'darkBlueColor' : "#031738",
        'greyColor' : "#80909D",
        'blueColor' : "#2487EC",
        'blackColor' : "#2D2C31",
        'navtext' : "#2387ea",
      },
      fontFamily: {
        'nunito': ['Nunito', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [],
};
