import apiClient from './apiClient.js';

class QuizService {
  /**
   * Загружает полную структуру квиза с сервера.
   * @param {number} id - ID квиза для загрузки.
   * @returns {Promise<object>} - Промис, который разрешается данными квиза.
   */
  getQuizById(id) {
    return apiClient.get(`/api/v1/quizzes/${id}`);
  }
}

// Экспортируем синглтон-экземпляр сервиса.
export default new QuizService();