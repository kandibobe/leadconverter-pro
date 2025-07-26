import apiClient from './apiClient.js'

class AdminLeadService {
  getLeads() {
    return apiClient.get('/api/v1/leads/')
  }
}

export default new AdminLeadService()
