<!-- frontend/src/views/admin/LeadsView.vue -->
<template>
  <div>
    <h1>Управление лидами</h1>
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="leads.length" class="leads-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Итоговая стоимость</th>
          <th>Дата создания</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lead in leads" :key="lead.id">
          <td>{{ lead.id }}</td>
          <td>{{ lead.email }}</td>
          <td>{{ formatCurrency(lead.final_price) }}</td>
          <td>{{ formatDate(lead.created_at) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else-if="!loading">
      <p>Лидов пока нет.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import adminLeadService from '../../services/adminLead.service.js'

const leads = ref([])
const loading = ref(true)
const error = ref(null)

const fetchLeads = async () => {
  try {
    const response = await adminLeadService.getLeads()
    leads.value = response.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value)
}

const formatDate = (dateString) => {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}

onMounted(fetchLeads)
</script>

<style scoped>
.leads-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
.leads-table th,
.leads-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}
.leads-table th {
  background-color: #ecf0f1;
  font-weight: bold;
  color: #2c3e50;
}
.leads-table tbody tr:hover {
  background-color: #f9f9f9;
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
