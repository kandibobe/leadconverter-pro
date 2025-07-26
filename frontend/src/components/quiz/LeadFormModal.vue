<script setup>
import { ref } from 'vue';
import { useQuizStore } from '../../stores/quiz.store.js';

const quizStore = useQuizStore();
const email = ref('');

function closeModal() {
  quizStore.closeLeadModal();
}

async function handleSubmit() {
  if (!email.value) {
    quizStore.leadSubmissionError = "Email не может быть пустым.";
    return;
  }
  await quizStore.submitLead(email.value);
}
</script>

<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-button" @click="closeModal">×</button>
      <h3>Получить детализированную смету</h3>
      <p>Введите ваш email, и мы отправим подробный расчет со всеми работами и материалами.</p>
      <form @submit.prevent="handleSubmit">
        <input
          v-model="email"
          type="email"
          placeholder="your@email.com"
          required
          class="email-input"
        />
        <div v-if="quizStore.leadSubmissionError" class="error-text">
          {{ quizStore.leadSubmissionError }}
        </div>
        <button type="submit" class="submit-button" :disabled="quizStore.isSubmittingLead">
          <span v-if="quizStore.isSubmittingLead">Отправка...</span>
          <span v-else>Получить смету</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Стили для модального окна */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: flex; justify-content: center; align-items: center; z-index: 100; }
.modal-content { background: white; padding: 2rem; border-radius: 8px; width: 90%; max-width: 500px; position: relative; }
.close-button { position: absolute; top: 10px; right: 10px; background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.email-input { width: 100%; padding: 0.75rem; margin: 1rem 0; border: 1px solid #ccc; border-radius: 4px; }
.submit-button { width: 100%; padding: 0.75rem; background-color: #42b983; color: white; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
.submit-button:disabled { background-color: #aaa; }
.error-text { color: red; font-size: 0.9rem; }
</style>
