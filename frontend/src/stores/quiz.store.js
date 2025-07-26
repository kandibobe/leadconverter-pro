// /frontend/src/stores/quiz.store.js

import { defineStore } from 'pinia';
import axios from 'axios';

// Настраиваем базовый URL для нашего API
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // URL нашего бэкенда
  headers: {
    'Content-Type': 'application/json',
  },
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
        this.error = 'Не удалось загрузить квиз. Попробуйте позже.';
        console.error(err);
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
    },
  },
});