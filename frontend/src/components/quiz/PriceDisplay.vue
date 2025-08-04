<script setup>
import { computed } from 'vue'
import { useQuizStore } from '../../stores/quiz.store.js'

const quizStore = useQuizStore()
const formattedPrice = computed(() =>
  new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
  }).format(quizStore.totalPrice)
)
</script>

<template>
  <div>
    <span>Предварительная стоимость:</span>
    <span>{{ formattedPrice }}</span>
  </div>
</template>
