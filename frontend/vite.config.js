import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Use root base for Netlify, and repository base for GitHub Pages
  base: process.env.NETLIFY ? '/' : '/Sudoku_Game/',
  server: {
    host: '127.0.0.1',
    port: 3000
  }
})
