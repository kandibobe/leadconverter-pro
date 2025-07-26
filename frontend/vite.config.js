// vite.config.js

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// Используем встроенные модули Node.js для работы с путями
import { fileURLToPath, URL } from 'url'

export default defineConfig({
  plugins: [vue()],

  // 1. Настраиваем АЛИАСЫ - это решит проблему с ../../
  resolve: {
    alias: {
      // '@' теперь всегда будет указывать на папку /src внутри проекта
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  // 2. Настраиваем СЕРВЕР для корректной работы внутри Docker
  server: {
    // Слушать на всех сетевых интерфейсах внутри контейнера
    host: '0.0.0.0', 
    // Убедитесь, что этот порт совпадает с тем, что вы пробрасываете в docker-compose.yml
    port: 5173, 
    hmr: {
      // Это нужно, чтобы Hot Module Replacement (автообновление) работало
      // и знало, на какой порт обращаться в браузере.
      clientPort: 5173 
    }
  }
})