import axios from 'axios';

// Создаем экземпляр axios с базовой конфигурацией.
// Это лучшая практика, чтобы не настраивать URL и заголовки в каждом запросе.
const apiBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  // URL нашего бэкенда берется из переменной окружения VITE_API_BASE_URL,
  // которую мы определили в файле .env в корне проекта.
  baseURL: apiBaseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Экспортируем созданный экземпляр, чтобы использовать его в других частях приложения.
export default apiClient;