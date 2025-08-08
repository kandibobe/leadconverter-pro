import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import federation from '@originjs/vite-plugin-federation';

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'quiz-shell',
      remotes: {
        builder: 'http://localhost:5001/assets/remoteEntry.js',
        admin: 'http://localhost:5002/assets/remoteEntry.js',
      },
      shared: ['vue', 'vue-router', 'pinia', 'axios'],
    }),
  ],
  build: {
    target: 'esnext',
  },
});

