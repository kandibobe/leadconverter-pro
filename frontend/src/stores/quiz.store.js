import { defineStore } from 'pinia';
import quizService from '../services/quiz.service.js';
import leadService from '../services/lead.service.js';

const getInitialState = () => ({
  quizData: null,
  isLoading: false,
  error: null,
  selectedOptions: {},
  area: 50,
  currentQuestionIndex: 0,
  isLeadModalVisible: false,
  isSubmittingLead: false,
  leadSubmissionError: null,
  isLeadSubmittedSuccessfully: false,
});

export const useQuizStore = defineStore('quiz', {
  state: getInitialState,
  getters: {
    currentQuestion: (state) => {
      if (!state.quizData) return null;
      return state.quizData.questions[state.currentQuestionIndex] || null;
    },
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
        state.quizData.questions.forEach(q => {

          const optionId = state.selectedOptions[q.id] ?? null;
          answers.push({
            question_id: q.id,
            option_id: optionId,
            value: q.question_type === 'slider' ? state.area : null,
          });

        });
      }
      return {
        quiz_id: state.quizData ? state.quizData.id : null,

        client_email: null,

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
        this.currentQuestionIndex = 0;
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
    nextQuestion() {
      if (this.quizData && this.currentQuestionIndex < this.quizData.questions.length) {
        this.currentQuestionIndex += 1;
      }
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
    async submitLead(email) {
      this.isSubmittingLead = true;
      this.leadSubmissionError = null;
      try {
        const payload = { ...this.leadPayload, client_email: email };
        await leadService.create(payload);
        this.closeLeadModal();
        this.isLeadSubmittedSuccessfully = true;
      } catch (error) {
        console.error("Lead submission failed:", error);
        this.leadSubmissionError = "Произошла ошибка. Пожалуйста, проверьте email и попробуйте снова.";
      } finally {
        this.isSubmittingLead = false;
      }
    },
  },
});
