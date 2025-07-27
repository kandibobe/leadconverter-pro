import { defineStore } from 'pinia';
import apiClient from '@/services/apiClient.js';
import { debounce } from 'lodash-es'; // Для умной отправки запросов

export const useQuizStore = defineStore('quiz', {
  state: () => ({
    quiz: null,
    currentQuestionIndex: 0,
    answers: [],
    isLoading: false,
    error: null,
    finalLead: null,
    preliminaryPrice: 0,
    isCalculating: false,
  }),

  getters: {
    currentQuestion: (state) => state.quiz?.questions?.[state.currentQuestionIndex] ?? null,
    isQuizFinished: (state) => state.quiz ? state.currentQuestionIndex >= state.quiz.questions.length : false,
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
        this.preliminaryPrice = 0;
      } catch (err) {
        this.error = 'Не удалось загрузить квиз. Попробуйте позже.';
        console.error('Fetch Quiz Error:', err);
      } finally {
        this.isLoading = false;
      }
    },

    selectAnswer(answerPayload) {
      const existingAnswerIndex = this.answers.findIndex(a => a.question_id === answerPayload.question_id);
      if (existingAnswerIndex > -1) {
        this.answers[existingAnswerIndex] = answerPayload;
      } else {
        this.answers.push(answerPayload);
      }

      if (answerPayload.option_id) { // Переходим дальше только если это не слайдер
          if (this.currentQuestionIndex < this.quiz.questions.length) {
              this.currentQuestionIndex++;
          }
      }
      this.debouncedCalculatePrice();
    },
    
    // Дебаунс, чтобы не слать запрос на каждый чих слайдера
    debouncedCalculatePrice: debounce(async function() {
        if (!this.quiz) return;
        this.isCalculating = true;
        try {
            const response = await apiClient.post('/quizzes/calculate', {
                quiz_id: this.quiz.id,
                client_email: 'temp@example.com', // email не важен для расчета
                answers: this.answers,
            });
            this.preliminaryPrice = response.data;
        } catch (error) {
            console.error('Price calculation error:', error);
        } finally {
            this.isCalculating = false;
        }
    }, 300), // Задержка в 300 мс

    async submitLead(clientEmail) {
        this.isLoading = true;
        this.error = null;
        const leadData = {
            quiz_id: this.quiz.id,
            client_email: clientEmail,
            answers: this.answers,
        };
        try {
            const response = await apiClient.post('/leads/submit', leadData);
            this.finalLead = response.data;
        } catch (err) {
            this.error = 'Произошла ошибка при отправке данных.';
            console.error('Submit Lead Error:', err);
        } finally {
            this.isLoading = false;
        }
    },
  },
});