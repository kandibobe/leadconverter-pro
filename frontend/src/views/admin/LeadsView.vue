<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/services/apiClient';

const leads = ref([]);
const isLoading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    const response = await apiClient.get('/leads/');
    leads.value = response.data;
  } catch (err) {
    error.value = 'Не удалось загрузить список лидов.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});

const formatDate = (dateString) => new Date(dateString).toLocaleString('ru-RU');
const formatCurrency = (value) => new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value);
</script>

<template>
  <div>
    <h1>Управление лидами</h1>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else-if="error" class="error-text">{{ error }}</div>
    <table v-else-if="leads.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Стоимость</th>
          <th>Дата</th>
          <th>Детали</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lead in leads" :key="lead.id">
          <td>{{ lead.id }}</td>
          <td>{{ lead.client_email }}</td>
          <td>{{ formatCurrency(lead.final_price) }}</td>
          <td>{{ formatDate(lead.created_at) }}</td>
          <td>
            <ul>
              <li v-for="(answer, question) in lead.answers_details" :key="question">
                <strong>{{ question }}:</strong> {{ answer }}
              </li>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else>Лидов пока нет.</div>
  </div>
</template>

<style scoped>
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid #ddd; padding: 8px; }
</style>