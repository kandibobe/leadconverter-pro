<script setup>
import { ref } from 'vue';
import { useQuizStore } from '@/stores/quiz.store';

const emit = defineEmits(['close']);
const quizStore = useQuizStore();
const clientEmail = ref('');
const emailError = ref('');

async function handleSubmit() {
  if (!clientEmail.value || !/^\S+@\S+\.\S+$/.test(clientEmail.value)) {
    emailError.value = 'Пожалуйста, введите корректный email.';
    return;
  }
  emailError.value = '';
  await quizStore.submitLead(clientEmail.value);
  // После успешной отправки можно показать сообщение или закрыть окно
  if (!quizStore.error) {
    // Можно добавить состояние "успешно отправлено"
    emit('close');
  }
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-content">
      <button @click="emit('close')" class="close-button">×</button>
      <div v-if="!quizStore.finalLead">
        <h3>Получить детализированную смету</h3>
        <p>Введите ваш email, и мы отправим подробный расчет.</p>
        <form @submit.prevent="handleSubmit">
          <input type="email" v-model="clientEmail" placeholder="your@email.com" required />
          <p v-if="emailError" class="error-text">{{ emailError }}</p>
          <p v-if="quizStore.error" class="error-text">{{ quizStore.error }}</p>
          <button type="submit" :disabled="quizStore.isLoading">
            {{ quizStore.isLoading ? 'Отправка...' : 'Получить смету' }}
          </button>
        </form>
      </div>
      <div v-else class="success-message">
        <h3>Отлично!</h3>
        <p>Ваша смета успешно отправлена на адрес {{ quizStore.finalLead.client_email }}.</p>
        <button @click="emit('close')">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Стили для модального окна */
</style>