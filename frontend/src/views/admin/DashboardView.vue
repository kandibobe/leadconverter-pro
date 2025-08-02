<template>
  <div class="dashboard-view">
    <h1 class="dashboard-title">Панель управления</h1>

    <div v-if="isLoading" class="loading-container">
      <Spinner />
      <p>Загружаем метрики...</p>
    </div>

    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
    </div>

    <div v-if="metrics && !isLoading" class="metrics-grid">
      <div class="metric-card">
        <h2 class="metric-value">{{ metrics.leads_count }}</h2>
        <p class="metric-label">Всего лидов</p>
        <span class="metric-icon">👥</span>
      </div>
      <div class="metric-card">
        <h2 class="metric-value">{{ formatCurrency(metrics.average_check) }}</h2>
        <p class="metric-label">Средний чек</p>
        <span class="metric-icon">💰</span>
      </div>
      <div class="metric-card coming-soon">
        <h2 class="metric-value">{{ metrics.quiz_views }}</h2>
        <p class="metric-label">Просмотры квиза</p>
        <span class="metric-icon">👁️</span>
        <div class="soon-badge">v1.5</div>
      </div>
      <div class="metric-card coming-soon">
        <h2 class="metric-value">{{ metrics.calculations_started }}</h2>
        <p class="metric-label">Начато расчетов</p>
        <span class="metric-icon">🚀</span>
        <div class="soon-badge">v1.5</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DashboardService from '@/services/dashboard.service.js';
import Spinner from '@/components/common/Spinner.vue';

const metrics = ref(null);
const isLoading = ref(true);
const error = ref(null);

const fetchMetrics = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    const response = await DashboardService.getMetrics();
    metrics.value = response.data;
  } catch (err) {
    console.error('Failed to fetch dashboard metrics:', err);
    error.value = 'Не удалось загрузить данные для панели управления. Пожалуйста, попробуйте позже.';
  } finally {
    isLoading.value = false;
  }
};

const formatCurrency = (value) => {
  if (typeof value !== 'number') return '0 ₽';
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

onMounted(fetchMetrics);
</script>

<style scoped>
.dashboard-view {
  padding: 2rem;
  background-color: #f9fafb;
  min-height: 100%;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 2rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #6b7280;
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.metric-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

.metric-label {
  color: #6b7280;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 2.25rem;
  font-weight: 800;
  color: #111827;
  line-height: 1.1;
}

.metric-icon {
  position: absolute;
  right: 1rem;
  top: 1rem;
  font-size: 2.5rem;
  opacity: 0.1;
  transform: rotate(-10deg);
}

.metric-card.coming-soon {
  opacity: 0.6;
  background-color: #f3f4f6;
}

.soon-badge {
  position: absolute;
  top: 8px;
  right: -30px;
  background-color: #8b5cf6;
  color: white;
  padding: 2px 30px;
  font-size: 0.7rem;
  font-weight: 600;
  transform: rotate(45deg);
  text-align: center;
}
</style>