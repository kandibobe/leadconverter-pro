import apiClient from './apiClient.js'

class HistoryService {
  getLeadHistory(id) {
    return apiClient.get(`/api/v1/leads/${id}/history`)
  }

  rollbackLead(id, eventId) {
    return apiClient.post(`/api/v1/leads/${id}/rollback/${eventId}`)
  }

  getQuizHistory(id) {
    return apiClient.get(`/api/v1/quizzes/${id}/history`)
  }

  rollbackQuiz(id, eventId) {
    return apiClient.post(`/api/v1/quizzes/${id}/rollback/${eventId}`)
  }
}

export default new HistoryService()
