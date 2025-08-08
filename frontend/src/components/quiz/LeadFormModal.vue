<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useQuizStore } from '../../stores/quiz.store.js';
import logger from '../../utils/logger.js';
import emitter from '../../utils/eventBus.js';

const quizStore = useQuizStore();
const email = ref('');
const errorMessage = ref('');
const successMessage = ref('');
let debounceTimer = null;

function closeModal() {
  quizStore.closeLeadModal();
}
 clearMessages();

function clearMessages() {
  errorMessage.value = '';
  successMessage.value = '';
}

function validateEmail(value) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(value);
}

async function submit() {
  if (!email.value) {
    errorMessage.value = 'Email не может быть пустым.';
    return;
}
if (!validateEmail(email.value)) {
    errorMessage.value = 'Некорректный формат email.';
    return;
  }
  logger.log('Submitting lead form', { email: email.value });
  await quizStore.submitLead(email.value);
}

function handleSubmit() {
  if (debounceTimer) return;
  debounceTimer = setTimeout(() => (debounceTimer = null), 1000);
  submit();
}

function onLeadSubmitted() {
  successMessage.value = 'Смета отправлена! Проверьте email.';
  errorMessage.value = '';
  email.value = '';
  setTimeout(() => {
    closeModal();
    successMessage.value = '';
  }, 2000);
}

function onLeadError(message) {
  errorMessage.value = message;
}

onMounted(() => {
  emitter.on('lead-submitted', onLeadSubmitted);
  emitter.on('lead-submission-error', onLeadError);
});

onUnmounted(() => {
  emitter.off('lead-submitted', onLeadSubmitted);
  emitter.off('lead-submission-error', onLeadError);
});
</script>

<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <button class="close-button" @click="closeModal">×</button>
      <h3>Получить детализированную смету</h3>
      <p>Введите ваш email, и мы отправим подробный расчет со всеми работами и материалами.</p>
      <form @submit.prevent="handleSubmit">
        <input
          v-model="quizStore.clientEmail"
          type="email"
          placeholder="your@email.com"
          required
          class="email-input"
        />
        <div v-if="errorMessage" class="error-text">
          {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="success-text">
          {{ successMessage }}
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
.success-text { color: green; font-size: 0.9rem; }
</style>