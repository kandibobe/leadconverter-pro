<template>
  <div class="ai-insights">
    <h2>AI-insights</h2>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="insights">
      <p><strong>Сегмент:</strong> {{ insights.segment }}</p>
      <p><strong>Что спросить дальше:</strong></p>
      <ul>
        <li v-for="q in insights.next_questions" :key="q">{{ q }}</li>
      </ul>
      <p><strong>Прогноз LTV:</strong> {{ formatCurrency(insights.ltv_prediction) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import aiService from '@/services/ai.service.js'

const insights = ref(null)
const loading = ref(true)

const fetchInsights = async () => {
  try {
    const payload = { final_price: 100000, answers_details: {} }
    const response = await aiService.getInsights(payload)
    insights.value = response.data
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

onMounted(fetchInsights)
</script>

<style scoped>
.ai-insights {
  margin-top: 20px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}
.ai-insights ul {
  list-style: disc;
  margin-left: 20px;
}
</style>
