<!-- /frontend/src/views/QuizView.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz.store';

import QuestionCard from '@/components/quiz/QuestionCard.vue';
import LeadFormModal from '@/components/quiz/LeadFormModal.vue';
import PriceDisplay from '@/components/quiz/PriceDisplay.vue';
import Spinner from '@/components/quiz/ui/Spinner.vue';

const quizStore = useQuizStore();
const showModal = ref(false);

onMounted(() => {
  quizStore.fetchQuiz(1);
});

function handleQuizCompleted() {
  showModal.value = true;
}

function handleLeadSubmitted() {
  showModal.value = false;
}
</script>

<template>
  <div class="quiz-container">
    <PriceDisplay v-if="quizStore.quizData" />
    <div v-if="quizStore.isLoading">
      <Spinner />
    </div>

    <div v-else-if="quizStore.error">
      <p class="error-message">Ошибка загрузки квиза: {{ quizStore.error }}</p>
    </div>

    <div v-else-if="quizStore.quizData">
      <h1>{{ quizStore.quizData.name }}</h1>
      <p>{{ quizStore.quizData.description }}</p>

      <QuestionCard
        v-if="quizStore.currentQuestion"
        :question="quizStore.currentQuestion"
      />

      <div v-else>
        <h2>Спасибо за ответы!</h2>
        <button @click="handleQuizCompleted">Получить смету</button>
      </div>
    </div>

    <LeadFormModal
      v-if="showModal"
      @close="showModal = false"
      @submitted="handleLeadSubmitted"
    />
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}
.error-message {
  color: red;
}
</style>