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

import { defineStore } from 'pinia';
import axios from 'axios';

// Настраиваем базовый URL для нашего API
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL нашего бэкенда
  headers: {
    'Content-Type': 'application/json',
  },
 main
});

export const useQuizStore = defineStore('quiz', {
  state: () => ({
    quiz: null,
    currentQuestionIndex: 0,
    answers: [],
    isLoading: false,
    error: null,
    finalLead: null,
  }),

  getters: {
    currentQuestion: (state) => {
      if (state.quiz && state.quiz.questions) {
        return state.quiz.questions[state.currentQuestionIndex];
      }
      return null;
    },
    isQuizFinished: (state) => {
        if (!state.quiz) return false;
        return state.currentQuestionIndex >= state.quiz.questions.length;
    }
  },

  actions: {
    async fetchQuiz(quizId) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get(`/quizzes/${quizId}`);
        this.quiz = response.data;
        this.currentQuestionIndex = 0;
        this.answers = [];
      } catch (err) {
 codex/improve-error-handling-and-add-i18n-support

        this.error = 'Не удалось загрузить квиз. Попробуйте позже.';
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

    selectAnswer(answer) {
        // answer должен быть объектом { question_id, option_id }
        this.answers.push(answer);
        if (this.currentQuestionIndex < this.quiz.questions.length) {
            this.currentQuestionIndex++;
        }
    },
 codex/improve-error-handling-and-add-i18n-support
    async submitLead(email) {
      this.isSubmittingLead = true;
      this.leadSubmissionError = null;
      try {
        const payload = { ...this.leadPayload, email };
        await leadService.create(payload);
        this.closeLeadModal();
        this.isLeadSubmittedSuccessfully = true;
      } catch (error) {
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
    },
  },
});
