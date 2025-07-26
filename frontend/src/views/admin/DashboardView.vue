<!-- frontend/src/views/DashboardView.vue -->
<template>
  <div>
    <h1>Дашборд</h1>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="metrics" class="metrics-grid">
      <div class="metric-card">
        <div class="metric-value">{{ metrics.total_leads }}</div>
        <div class="metric-label">Всего лидов</div>
      </div>
      <div class="metric-card">
        <div class="metric-value">{{ formatCurrency(metrics.average_check) }}</div>
        <div class="metric-label">Средний чек</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import dashboardService from '../services/dashboard.service.js'

const metrics = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchMetrics = async () => {
  try {
    const response = await dashboardService.getMetrics()
    metrics.value = response.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

onMounted(fetchMetrics)
</script>

<style scoped>
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
.metric-card {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}
.metric-value {
  font-size: 3em;
  font-weight: bold;
  color: #2c3e50;
}
.metric-label {
  font-size: 1.1em;
  color: #7f8c8d;
  margin-top: 10px;
}
.loading,
.error {
  margin-top: 20px;
  font-size: 1.2em;
}
.error {
  color: #e74c3c;
}
</style>
