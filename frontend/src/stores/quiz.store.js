 codex/improve-error-handling-and-add-i18n-support
 codex/improve-error-handling-and-add-i18n-support
// @ts-check
import { defineStore } from 'pinia';
import quizService from '../services/quiz.service.js';
import leadService from '../services/lead.service.js';
/** @typedef {import('../types.js').Quiz} Quiz */
/** @typedef {import('../types.js').LeadData} LeadData */

const getInitialState = () => ({
  /** @type {Quiz|null} */
  quizData: null,
  isLoading: false,
  /** @type {string|null} */
  error: null,
  selectedOptions: {},
  area: 50,
  isLeadModalVisible: false,
  isSubmittingLead: false,
  /** @type {string|null} */
  leadSubmissionError: null,
  isLeadSubmittedSuccessfully: false,

// /frontend/src/stores/quiz.store.js


 main
import { defineStore } from 'pinia';
import quizService from '../services/quiz.service.js';
import leadService from '../services/lead.service.js';

 codex/improve-error-handling-and-add-i18n-support
// Настраиваем базовый URL для нашего API
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL нашего бэкенда
  headers: {
    'Content-Type': 'application/json',
  },
 main
=======
const getInitialState = () => ({
  quizData: null,
  isLoading: false,
  error: null,
  selectedOptions: {},
  area: 50,
  isLeadModalVisible: false,
  isSubmittingLead: false,
  leadSubmissionError: null,
  isLeadSubmittedSuccessfully: false,
 main
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
      const answers_data = {};
      if (state.quizData) {
        state.quizData.questions.forEach(q => {
          if (q.question_type === 'slider') {
            answers_data[q.text] = `${state.area} м²`;
          } else {
            const optionId = state.selectedOptions[q.id];
            if (optionId) {
              const option = q.options.find(o => o.id === optionId);
              answers_data[q.text] = option ? option.text : 'Не выбрано';
            }
          }
        });
      }
      return {
        final_price: state.totalPrice,
        answers_data,
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
 codex/improve-error-handling-and-add-i18n-support
 codex/improve-error-handling-and-add-i18n-support

        this.error = 'Не удалось загрузить квиз. Попробуйте позже.';
 main

        this.error = 'Не удалось загрузить квиз.';
 main
        console.error(err);
        if (!err.response) {
          this.error = 'NETWORK';
        } else if (err.response.status === 404) {
          this.error = 'NOT_FOUND';
        } else {
          this.error = 'UNKNOWN';
        }
      } finally {
        this.isLoading = false;
      }
    },
    selectOption(questionId, optionId) {
      this.selectedOptions[questionId] = optionId;
    },
 codex/improve-error-handling-and-add-i18n-support
 codex/improve-error-handling-and-add-i18n-support

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
 main
    async submitLead(email) {
      this.isSubmittingLead = true;
      this.leadSubmissionError = null;
      try {
        const payload = { ...this.leadPayload, email };
        await leadService.create(payload);
        this.closeLeadModal();
        this.isLeadSubmittedSuccessfully = true;
      } catch (error) {
 codex/improve-error-handling-and-add-i18n-support
        console.error('Lead submission failed:', error);
        this.leadSubmissionError = error.response ? 'SUBMIT' : 'NETWORK';
      } finally {
        this.isSubmittingLead = false;
      }


    async submitLead(clientEmail) {
        this.isLoading = true;
        this.error = null;
        const leadData = {
            quiz_id: this.quiz.id,
            client_email: clientEmail,
            answers: this.answers,
        };

        try {
            const response = await apiClient.post('/leads', leadData);
            this.finalLead = response.data;
            console.log('Лид успешно создан:', this.finalLead);
        } catch (err) {
            this.error = 'Произошла ошибка при отправке данных.';
            console.error(err);
        } finally {
            this.isLoading = false;
        }
 main

        console.error("Lead submission failed:", error);
        this.leadSubmissionError = "Произошла ошибка. Пожалуйста, проверьте email и попробуйте снова.";
      } finally {
        this.isSubmittingLead = false;
      }
 main
    },
  },
});
