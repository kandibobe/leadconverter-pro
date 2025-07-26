<!-- /frontend/src/views/admin/DashboardView.vue -->

<script setup>
import { ref, onMounted } from 'vue';

// БЫЛО:
// import dashboardService from '../../services/dashboard.service.js';

// СТАЛО:
import dashboardService from '@/services/dashboard.service.js'; // <-- ИСПОЛЬЗУЕМ АЛИАС '@'

// Здесь будет логика для получения данных для дашборда
const stats = ref(null);
const isLoading = ref(true);
const error = ref(null);

onMounted(async () => {
  try {
    // В будущем здесь будет вызов функции для получения статистики
    // stats.value = await dashboardService.getStats();
    console.log('DashboardView смонтирован.');
  } catch (err) {
    error.value = 'Не удалось загрузить статистику.';
  } finally {
    isLoading.value = false;
  }
});
</script>