import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia'; // <-- ИМПОРТИРУЕМ PINIA
import { createI18n } from 'vue-i18n';

import App from './App.vue';
import router from './router';
import ru from './locales/ru.json';
import en from './locales/en.json';

const app = createApp(App);

// Инициализация i18n
const i18n = createI18n({
  locale: 'ru',
  fallbackLocale: 'en',
  messages: { ru, en },
});

// ИСПОЛЬЗУЕМ PINIA
// Эта строка регистрирует Pinia в приложении.
// Без нее ни один store работать не будет.
app.use(createPinia());
app.use(router);
app.use(i18n); // подключаем i18n

app.mount('#app');
