<script setup>
import { computed } from 'vue';
import { useQuizStore } from '../../stores/quiz.store.js';

const props = defineProps({
  option: { type: Object, required: true },
  questionId: { type: Number, required: true },
});

const quizStore = useQuizStore();

// Проверяем, выбрана ли эта опция в store
const isSelected = computed(() => {
  return quizStore.selectedOptions[props.questionId] === props.option.id;
});

function select() {
  // Вызываем action из store, чтобы обновить состояние
  quizStore.selectOption(props.questionId, props.option.id);
}
</script>

<template>
  <li
    class="option-item"
    :class="{ 'is-selected': isSelected }"
    @click="select"
  >
    {{ option.text }}
  </li>
</template>

<style scoped>
.option-item {
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}
.option-item:hover {
  border-color: #42b983;
  box-shadow: 0 0 10px rgba(66, 185, 131, 0.2);
}
.is-selected {
  background-color: #42b983;
  color: white;
  border-color: #33a06f;
  font-weight: bold;
}
</style>
