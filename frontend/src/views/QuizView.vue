<script setup>
import { onMounted, computed, ref, watch } from 'vue';
import { useQuizStore } from '@/stores/quiz.store';
import LeadFormModal from '@/components/LeadFormModal.vue'; // <-- НОВОЕ
const isModalOpen = ref(false); // <-- НОВОЕ

const quizStore = useQuizStore();

const quiz = computed(() => quizStore.quiz);
const currentQuestion = computed(() => quizStore.currentQuestion);
const isLoading = computed(() => quizStore.isLoading);
const error = computed(() => quizStore.error);
const isQuizFinished = computed(() => quizStore.isQuizFinished);
const preliminaryPrice = computed(() => quizStore.preliminaryPrice);

const sliderValue = ref(50); // Начальное значение для слайдера

onMounted(() => {
  quizStore.fetchQuiz(1);
});

watch(currentQuestion, (newQuestion) => {
  if (newQuestion?.question_type === 'slider') {
    const existingAnswer = quizStore.answers.find(a => a.question_id === newQuestion.id);
    sliderValue.value = existingAnswer?.value || 50;
  }
});

function handleAnswerSelect(optionId) {
  quizStore.selectAnswer({
    question_id: currentQuestion.value.id,
    option_id: optionId,
  });
}

function handleSliderChange() {
  quizStore.selectAnswer({
    question_id: currentQuestion.value.id,
    value: sliderValue.value,
  });
}
</script>

<template>
  <main class="quiz-container">
    <div v-if="isLoading" class="state-info">Загружаем квиз...</div>
    <div v-else-if="error" class="state-info error">{{ error }}</div>
    <div v-else-if="quiz" class="quiz-content">
      <header class="quiz-header">
        <h1>{{ quiz.title }}</h1>
        <p>{{ quiz.description }}</p>
      </header>

      <div v-if="!isQuizFinished && currentQuestion" class="question-block">
        <h3>Вопрос {{ currentQuestion.order }}/{{ quiz.questions.length }}: {{ currentQuestion.text }}</h3>
        <p v-if="currentQuestion.description" class="description">{{ currentQuestion.description }}</p>
        
        <div v-if="currentQuestion.question_type === 'single-choice'" class="options-list">
          <button v-for="option in currentQuestion.options" :key="option.id" @click="handleAnswerSelect(option.id)" class="option-button">
            {{ option.text }}
          </button>
        </div>

        <div v-if="currentQuestion.question_type === 'slider'" class="slider-container">
          <input type="range" min="10" max="200" v-model="sliderValue" @input="handleSliderChange" class="slider" />
          <div class="slider-value">{{ sliderValue }} м²</div>
        </div>
      </div>

      <div v-else-if="isQuizFinished" class="quiz-finished-block">
        <h2>Спасибо! Расчет готов.</h2>
        <p>Введите ваш email, чтобы получить детализированную смету на почту.</p>
        <!-- TODO: Компонент LeadFormModal -->
      </div>

      <div class="price-display">
        Предварительная стоимость: <strong>{{ new Intl.NumberFormat('ru-RU').format(preliminaryPrice) }} ₽</strong>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* Стили остаются те же, что и в прошлый раз, можно добавить стили для слайдера */
.slider-container { margin-top: 2rem; text-align: center; }
.slider { width: 100%; }
.slider-value { font-size: 1.2rem; font-weight: bold; margin-top: 0.5rem; }
.price-display {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f9f9f9;
  border-top: 2px solid #4CAF50;
  text-align: center;
  font-size: 1.5rem;
}
</style>