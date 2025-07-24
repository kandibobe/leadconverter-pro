<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useQuizStore } from '../stores/quiz.store.js';

import PriceDisplay from '../components/quiz/PriceDisplay.vue';
import QuestionCard from '../components/quiz/QuestionCard.vue';

const route = useRoute();
const quizStore = useQuizStore();

onMounted(() => {
  // Сбрасываем состояние перед загрузкой нового квиза.
  // Это гарантирует, что не останется старых ответов.
  quizStore.reset();
  
  // Запускаем загрузку данных
  quizStore.fetchQuiz(route.params.id);
});
</script>

<template>
  <div class="quiz-container">
    <div v-if="quizStore.isLoading" class="loading-indicator">Загрузка...</div>
    <div v-else-if="quizStore.error" class="error-message">{{ quizStore.error }}</div>

    <div v-else-if="quizStore.quizData" class="quiz-content">
      <PriceDisplay />

      <header class="quiz-header">
        <h1>{{ quizStore.quizData.title }}</h1>
      </header>

      <QuestionCard
        v-for="question in quizStore.quizData.questions"
        :key="question.id"
        :question="question"
      />
    </div>
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: #f4f7f9;
}
.quiz-header { text-align: center; margin-bottom: 2rem; }
.loading-indicator, .error-message { text-align: center; font-size: 1.2rem; padding: 3rem; color: #333; }
</style>