import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia'; // <-- ИМПОРТИРУЕМ PINIA

import App from './App.vue';
import router from './router';

const app = createApp(App);

// ИСПОЛЬЗУЕМ PINIA
// Эта строка регистрирует Pinia в приложении.
// Без нее ни один store работать не будет.
app.use(createPinia());
app.use(router);

app.mount('#app');
