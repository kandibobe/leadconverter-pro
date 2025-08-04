<script setup>
import OptionItem from './OptionItem.vue';
import { useQuizStore } from '../../stores/quiz.store.js';

defineProps({
  question: { type: Object, required: true },
});

const quizStore = useQuizStore();

// Обработчики для слайдера
function handleSliderInput(event) {
  quizStore.setArea(parseInt(event.target.value));
}

function handleSliderChange() {
  quizStore.nextQuestion();
}
</script>

<template>
  <div class="question-card">
    <h3>{{ question.order }}. {{ question.text }}</h3>
    <p v-if="question.description" class="question-description">
      <span class="info-icon">i</span> {{ question.description }}
    </p>

    <!-- Если тип вопроса - выбор одной опции -->
    <ul v-if="question.question_type === 'single-choice'" class="options-list">
      <OptionItem
        v-for="option in question.options"
        :key="option.id"
        :option="option"
        :question-id="question.id"
      />
    </ul>

    <!-- Если тип вопроса - слайдер -->
    <div v-if="question.question_type === 'slider'" class="slider-container">
      <input
        type="range"
        min="20"
        max="200"
        :value="quizStore.area"
        @input="handleSliderInput"
        @change="handleSliderChange"
        class="slider"
      />
      <div class="slider-value">{{ quizStore.area }} м²</div>
    </div>
  </div>
</template>

<style scoped>
/* Стили скопированы из старого QuizView и улучшены */
.question-card {
  margin-bottom: 2rem;
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fff;
}
.question-description {
  font-size: 0.9rem; color: #757575; background-color: #f9f9f9;
  padding: 0.5rem; border-radius: 4px;
}
.info-icon {
  display: inline-block; width: 16px; height: 16px; line-height: 16px;
  text-align: center; border-radius: 50%; background-color: #1e88e5;
  color: white; font-style: normal; font-weight: bold; margin-right: 8px;
}
.options-list { list-style-type: none; padding: 0; margin-top: 1rem; }
.slider-container { margin-top: 1.5rem; text-align: center; }
.slider { width: 100%; }
.slider-value { margin-top: 0.5rem; font-size: 1.2rem; font-weight: bold; }
</style>