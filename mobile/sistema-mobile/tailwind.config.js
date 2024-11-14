module.exports = {
  content: [
    "./src/**/*.{html,ts}", // Certifique-se de incluir todos os arquivos HTML e TS
  ],
  theme: {
    extend: {
      colors: {
        primary: '#007bff',
        secondary: '#28a745',
        dark: '#34495e',
        light: '#f0f2f5',
      },
      borderRadius: {
        'lg': '1.5rem',
      },
      fontFamily: {
        sans: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
