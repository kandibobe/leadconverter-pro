 codex/improve-error-handling-and-add-i18n-support
<script setup>
import { onMounted, defineAsyncComponent } from 'vue';
import { useQuizStore } from '@/stores/quiz.store.js';
=======
<!-- /frontend/src/views/QuizView.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz.store';

// --- ФИНАЛЬНЫЕ, ПРАВИЛЬНЫЕ ПУТИ СОГЛАСНО ВАШЕМУ СКРИНШОТУ ---

// Эти компоненты лежат в /components/quiz/
 main
import QuestionCard from '@/components/quiz/QuestionCard.vue';
import PriceDisplay from '@/components/quiz/PriceDisplay.vue';
import LeadFormModal from '@/components/quiz/LeadFormModal.vue';
 codex/improve-error-handling-and-add-i18n-support
import { useI18n } from 'vue-i18n';

const Spinner = defineAsyncComponent(() => import('@/components/quiz/ui/Spinner.vue'));
=======
import PriceDisplay from '@/components/quiz/PriceDisplay.vue';

// А этот компонент лежит в /components/quiz/ui/
import Spinner from '@/components/quiz/ui/Spinner.vue';

 main

const { t } = useI18n();
const quizStore = useQuizStore();

onMounted(() => {
 codex/improve-error-handling-and-add-i18n-support
  quizStore.fetchQuiz(1);
});
</script>

<template>
  <div class="quiz-container">
    <Spinner v-if="quizStore.isLoading" />
    <template v-else>
      <p v-if="quizStore.error" class="error-message">
        {{ t(`errors.${quizStore.error}`) }}
      </p>
      <div v-else>
        <PriceDisplay />
        <div v-for="question in quizStore.quizData?.questions" :key="question.id">
          <QuestionCard :question="question" />
        </div>
        <button class="estimate-btn" @click="quizStore.openLeadModal">
          {{ t('quiz.get_estimate') }}
        </button>
        <p v-if="quizStore.isLeadSubmittedSuccessfully" class="success-msg">
          {{ t('lead_modal.success') }}
        </p>
      </div>
    </template>
    <LeadFormModal v-if="quizStore.isLeadModalVisible" />
  </div>
</template>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
}
.error-message { color: red; margin: 1rem 0; }
.success-msg { color: green; margin-top: 1rem; }
.estimate-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>


  quizStore.fetchQuiz(1); 
});

function handleQuizCompleted() {
  showModal.value = true;
}

function handleLeadSubmitted() {
  showModal.value = false;
}
</script>
 main
