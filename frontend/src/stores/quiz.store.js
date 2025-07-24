import { defineStore } from 'pinia';
import quizService from '../services/quiz.service.js';

// Функция для получения начального состояния.
// Вынесена отдельно, чтобы легко переиспользовать ее в reset.
const getInitialState = () => ({
  quizData: null,
  isLoading: false,
  error: null,
  selectedOptions: {},
  area: 50,
});

export const useQuizStore = defineStore('quiz', {
  state: getInitialState,

  getters: {
    totalPrice: (state) => {
      if (!state.quizData) return 0;

      const basePricePerMeter = Object.values(state.selectedOptions).reduce((total, optionId) => {
        // Более надежный поиск опции во вложенной структуре
        for (const question of state.quizData.questions) {
          const option = question.options.find(o => o.id === optionId);
          if (option) {
            return total + option.price_impact;
          }
        }
        return total;
      }, 0);

      return basePricePerMeter * state.area;
    },
  },

  actions: {
    async fetchQuiz(id) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await quizService.getQuizById(id);
        this.quizData = response.data;
      } catch (err) {
        this.error = 'Не удалось загрузить квиз.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    selectOption(questionId, optionId) {
      this.selectedOptions[questionId] = optionId;
    },

    setArea(newArea) {
      this.area = newArea;
    },

    // НОВЫЙ ЭКШЕН ДЛЯ СБРОСА СОСТОЯНИЯ
    reset() {
      // Object.assign перезаписывает текущее состояние начальными значениями.
      Object.assign(this, getInitialState());
    },
  },
});