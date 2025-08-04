<script setup>
import OptionItem from './OptionItem.vue'
import { useQuizStore } from '../../stores/quiz.store.js'

defineProps({
  question: { type: Object, required: true }
})

const quizStore = useQuizStore()

function handleSliderChange(e) {
  quizStore.setArea(parseInt(e.target.value))
}
</script>

<template>
  <div>
    <h3>{{ question.order }}. {{ question.text }}</h3>
    <p v-if="question.description">{{ question.description }}</p>

    <ul v-if="question.question_type === 'single-choice'">
      <OptionItem
        v-for="option in question.options"
        :key="option.id"
        :option="option"
        :question-id="question.id"
      />
    </ul>

    <div v-else-if="question.question_type === 'slider'">
      <input
        type="range"
        min="20"
        max="200"
        :value="quizStore.area"
        @input="handleSliderChange"
      />
      <div>{{ quizStore.area }} м²</div>
    </div>
  </div>
</template>
