import { defineStore } from 'pinia';
import quizService from '../services/quiz.service.js';
import leadService from '../services/lead.service.js';
import logger from '../utils/logger.js';
import emitter from '../utils/eventBus.js';

const getInitialState = () => ({
  quizData: null,
  isLoading: false,
  error: null,
  selectedOptions: {},
  area: 50,
  clientEmail: '',
  isLeadModalVisible: false,
  isSubmittingLead: false,
});

export const useQuizStore = defineStore('quiz', {
  state: getInitialState,
  getters: {
    totalPrice: (state) => {
      if (!state.quizData) return 0;
      const basePricePerMeter = Object.values(state.selectedOptions).reduce((total, optionId) => {
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
    leadPayload: (state) => {
      const answers = [];
      if (state.quizData) {
        state.quizData.questions.forEach((q) => {
          if (q.question_type === 'slider') {
            answers.push({ question_id: q.id, value: state.area });
          } else {
            const optionId = state.selectedOptions[q.id];
            if (optionId) {
              answers.push({ question_id: q.id, option_id: optionId });
            }
          }
        });
      }
      return {
        quiz_id: state.quizData ? state.quizData.id : undefined,
        client_email: state.clientEmail,
        final_price: state.totalPrice,
        answers,
      };
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
        logger.error(err);
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
    reset() {
      Object.assign(this, getInitialState());
    },
    openLeadModal() {
      this.isLeadModalVisible = true;
    },
    closeLeadModal() {
      this.isLeadModalVisible = false;
    },
    async submitLead() {
      this.isSubmittingLead = true;
      try {
        await leadService.create(this.leadPayload);
        emitter.emit('lead-submitted');
      } catch (error) {
        logger.error('Lead submission failed:', error);
emitter.emit(
          'lead-submission-error',
          'Произошла ошибка. Пожалуйста, проверьте email и попробуйте снова.'
        );
      } finally {
        this.isSubmittingLead = false;
      }
    },
  },
});
