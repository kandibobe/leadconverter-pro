<!-- /app/src/views/QuizView.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz.store'; // <-- ИСПОЛЬЗУЕМ АЛИАС

// ИСПРАВЛЯЕМ ВСЕ ПУТИ НА АЛИАСЫ '@'
import QuestionCard from '@/components/quiz/QuestionCard.vue';
import LeadFormModal from '@/components/quiz/LeadFormModal.vue';
import Spinner from '@/components/Spinner.vue';  // <-- ИСПРАВЛЕННЫЙ ПУТЬ

const quizStore = useQuizStore();
const showModal = ref(false);

onMounted(() => {
  // Загружаем данные для квиза с ID=1 при монтировании компонента
  quizStore.fetchQuiz(1); 
});

function handleQuizCompleted() {
  showModal.value = true;
}

function handleLeadSubmitted() {
  showModal.value = false;
  // Здесь можно добавить логику "Спасибо за вашу заявку!"
  // Например, перенаправить на другую страницу
  // router.push('/thank-you');
}
</script>

<template>
  <div class="quiz-container">
    <div v-if="quizStore.isLoading">
      <Spinner />
    </div>
    
    <div v-else-if="quizStore.error">
      <p class="error-message">Ошибка загрузки квиза: {{ quizStore.error }}</p>
    </div>

    <div v-else-if="quizStore.quiz">
      <h1>{{ quizStore.quiz.name }}</h1>
      <p>{{ quizStore.quiz.description }}</p>
      
      <QuestionCard 
        v-if="quizStore.currentQuestion"
        :question="quizStore.currentQuestion"
        @answer-selected="quizStore.selectAnswer"
      />
      
      <div v-else>
        <h2>Спасибо за ответы!</h2>
        <button @click="handleQuizCompleted">Получить смету</button>
      </div>
    </div>

    <LeadFormModal 
      :show="showModal" 
      @close="showModal = false"
      @submitted="handleLeadSubmitted"
    />
  </div>
</template>

<style scoped>
/* Стили остаются без изменений */
.quiz-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}
.error-message {
  color: red;
}
</style>