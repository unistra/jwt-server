import { defineConfig } from 'vite'
import { resolve } from 'node:path'

export default defineConfig({
  // CORRECTION ICI : On s'aligne sur ton URL Django (/site_media/)
  base: '/site_media/dist/',

  build: {
    manifest: 'manifest.json',
    // Le chemin disque, lui, ne change pas
    outDir: resolve(__dirname, 'jwtserver/static/dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'jwtserver/static/js/jwtserver.js'),
        home: resolve(__dirname, 'jwtserver/static/js/home.js'),
        token: resolve(__dirname, 'jwtserver/static/js/token.js'),
      },
    },
  },

  server: {
    // Pour que Django puisse taper dans le serveur de dev Vite
    origin: 'http://localhost:5173',
  },
})
