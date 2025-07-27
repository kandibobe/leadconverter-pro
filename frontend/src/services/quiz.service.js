// @ts-check
import apiClient from './apiClient.js';
/** @typedef {import('../types.js').Quiz} Quiz */

class QuizService {
  /**
   * Fetch quiz structure by id
   * @param {number} id
   * @returns {Promise<import('axios').AxiosResponse<Quiz>>}
   */
  getQuizById(id) {
    return apiClient.get(`/api/v1/quizzes/${id}`);
  }
}

export default new QuizService();
