<script setup>
import { computed } from 'vue';
import { useQuizStore } from '../../stores/quiz.store.js';

const quizStore = useQuizStore();

// Используем computed, чтобы цена форматировалась красиво
const formattedPrice = computed(() => {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
  }).format(quizStore.totalPrice);
});
</script>

<template>
  <div class="price-display">
    <span class="price-label">Предварительная стоимость:</span>
    <span class="price-value">{{ formattedPrice }}</span>
  </div>
</template>

<style scoped>
.price-display {
  position: sticky;
  top: 0;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  text-align: center;
  z-index: 10;
  border-radius: 8px;
  margin-bottom: 2rem;
}
.price-label {
  margin-right: 1rem;
  font-size: 1.1rem;
}
.price-value {
  font-size: 1.8rem;
  font-weight: bold;
}
</style>
