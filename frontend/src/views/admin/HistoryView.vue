<template>
  <div>
    <h1>История изменений</h1>
    <div class="controls">
      <input v-model="leadId" placeholder="ID лида" />
      <button @click="fetchHistory">Загрузить</button>
    </div>
    <ul v-if="events.length">
      <li v-for="event in events" :key="event.id">
        {{ new Date(event.timestamp).toLocaleString() }}
      </li>
    </ul>
    <p v-else>Нет данных.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import historyService from '../../services/history.service.js'

const leadId = ref('')
const events = ref([])

const fetchHistory = async () => {
  if (!leadId.value) return
  const response = await historyService.getLeadHistory(leadId.value)
  events.value = response.data
}
</script>

<style scoped>
.controls {
  margin-bottom: 1rem;
}
input {
  margin-right: 0.5rem;
}
</style>
