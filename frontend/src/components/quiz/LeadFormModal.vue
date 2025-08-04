<script setup>
import { ref } from 'vue'
import { useQuizStore } from '../../stores/quiz.store.js'

const quizStore = useQuizStore()
const email = ref('')
const emit = defineEmits(['close', 'submitted'])

async function submit() {
  if (!email.value) return
  await quizStore.submitLead(email.value)
  emit('submitted')
}
</script>

<template>
  <div class="modal" @click.self="emit('close')">
    <form @submit.prevent="submit">
      <input v-model="email" type="email" required />
      <div v-if="quizStore.leadSubmissionError">{{ quizStore.leadSubmissionError }}</div>
      <button type="submit" :disabled="quizStore.isSubmittingLead">
        <span v-if="quizStore.isSubmittingLead">Отправка...</span>
        <span v-else>Получить смету</span>
      </button>
      <button type="button" @click="emit('close')">Закрыть</button>
    </form>
  </div>
</template>
