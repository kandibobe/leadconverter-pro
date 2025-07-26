<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useQuizStore } from '../stores/quiz.store.js';

// Импортируем все компоненты
import PriceDisplay from '../components/quiz/PriceDisplay.vue';
import QuestionCard from '../components/quiz/QuestionCard.vue';
import LeadFormModal from '../components/quiz/LeadFormModal.vue';
import Spinner from '../components/ui/Spinner.vue'; // <-- Импортируем спиннер

const route = useRoute();
const quizStore = useQuizStore();

onMounted(() => {
  quizStore.reset();
  quizStore.fetchQuiz(route.params.id);
});
</script>

<template>
  <div class="quiz-container">
    <LeadFormModal v-if="quizStore.isLeadModalVisible" />
    
    <!-- Используем спиннер вместо текста -->
    <Spinner v-if="quizStore.isLoading" />

    <div v-else-if="quizStore.error" class="error-message">{{ quizStore.error }}</div>

    <div v-else-if="quizStore.isLeadSubmittedSuccessfully" class="success-container">
      <h2>Спасибо!</h2>
      <p>Ваша заявка принята. Мы скоро свяжемся с вами и вышлем детализированную смету на ваш email.</p>
      <RouterLink to="/" class="back-to-home">Вернуться на главную</RouterLink>
    </div>

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
      <div class="actions-container">
        <button @click="quizStore.openLeadModal" class="get-estimate-button">
          Получить смету
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiz-container { position: relative; /* Нужно для позиционирования спиннера */ max-width: 800px; margin: 2rem auto; padding: 1rem; background-color: #f4f7f9; min-height: 300px; }
.quiz-header { text-align: center; margin-bottom: 2rem; }
.error-message { text-align: center; font-size: 1.2rem; padding: 3rem; color: #e53e3e; }
.actions-container { text-align: center; margin-top: 2rem; }
.get-estimate-button { padding: 1rem 2.5rem; font-size: 1.1rem; font-weight: bold; color: #fff; background-color: #1e88e5; border: none; border-radius: 8px; cursor: pointer; transition: background-color 0.3s ease; }
.get-estimate-button:hover { background-color: #1565c0; }
.success-container { text-align: center; padding: 4rem 2rem; background-color: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.success-container h2 { color: #42b983; }
.back-to-home { display: inline-block; margin-top: 2rem; padding: 0.75rem 1.5rem; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 4px; }
</style>