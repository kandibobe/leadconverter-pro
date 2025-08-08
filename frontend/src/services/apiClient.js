import axios from 'axios';

// Создаем экземпляр axios с базовой конфигурацией.
// Это лучшая практика, чтобы не настраивать URL и заголовки в каждом запросе.
const apiBaseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Определяем функцию для получения идентификатора арендатора из хранилища или конфигурации.
const getTenantId = () =>
  window.localStorage?.getItem('tenantId') || import.meta.env.VITE_TENANT_ID;

const apiClient = axios.create({
  // URL нашего бэкенда берется из переменной окружения VITE_API_BASE_URL,
  // которую мы определили в файле .env в корне проекта.
  baseURL: apiBaseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Перехватчик добавляет X-Tenant-ID в каждый запрос.
apiClient.interceptors.request.use((config) => {
  const tenantId = getTenantId();
  if (tenantId) {
    config.headers['X-Tenant-ID'] = tenantId;
  }
  return config;
});

// Экспортируем созданный экземпляр, чтобы использовать его в других частях приложения.
export default apiClient;