import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://backend:8000',   // имя сервиса в docker-сети
        changeOrigin: true,
        // если на бэке пути без /api — раскомментируйте переписывание
        // rewrite: (path) => path.replace(/^\/api/, ''),

        // отладочные хуки — видно, что реально уходит/приходит
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req) => console.log('› proxyReq', req.method, req.url))
          proxy.on('proxyRes', (proxyRes, req) => console.log('› proxyRes', proxyRes.statusCode, req.url))
          proxy.on('error', (err, req) => console.error('› proxyError', err?.message, req.url))
        }
      }
    }
  }
})
