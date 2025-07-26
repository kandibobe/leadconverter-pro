<!-- /frontend/src/views/QuizView.vue -->

<script setup>
import { ref, onMounted } from 'vue';
import { useQuizStore } from '@/stores/quiz.store';

// --- ФИНАЛЬНЫЕ, ПРАВИЛЬНЫЕ ПУТИ СОГЛАСНО ВАШЕМУ СКРИНШОТУ ---

// Эти компоненты лежат в /components/quiz/
import QuestionCard from '@/components/quiz/QuestionCard.vue';
import LeadFormModal from '@/components/quiz/LeadFormModal.vue';
import PriceDisplay from '@/components/quiz/PriceDisplay.vue';

// А этот компонент лежит в /components/quiz/ui/
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