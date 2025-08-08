import apiClient from './apiClient.js'

class AIService {
  getInsights(payload) {
    return apiClient.post('/api/v1/ai/insights', payload)
  }
}

export default new AIService()
